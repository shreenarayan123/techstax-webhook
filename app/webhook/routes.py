from flask import Blueprint, json, request, jsonify
from datetime import datetime, timezone
from app.extensions import mongo
import hmac
import hashlib
import os

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# Webhook secret for verification (optional but recommended)
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')


def verify_signature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256 signature."""
    if not WEBHOOK_SECRET:
        return True  # Skip verification if no secret is set
    
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


def parse_push_event(payload):
    """Parse GitHub push event payload."""
    ref = payload.get('ref', '')
    branch = ref.replace('refs/heads/', '') if ref.startswith('refs/heads/') else ref
    
    head_commit = payload.get('head_commit', {})
    commit_id = head_commit.get('id', '')[:7] if head_commit else ''
    
    pusher = payload.get('pusher', {})
    author = pusher.get('name', 'Unknown')
    
    return {
        'request_id': commit_id,
        'author': author,
        'action': 'PUSH',
        'from_branch': branch,
        'to_branch': branch,
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    }


def parse_pull_request_event(payload):
    """Parse GitHub pull request event payload."""
    action = payload.get('action', '')
    pr = payload.get('pull_request', {})
    
    pr_number = payload.get('number', '')
    author = pr.get('user', {}).get('login', 'Unknown')
    head_branch = pr.get('head', {}).get('ref', '')
    base_branch = pr.get('base', {}).get('ref', '')
    merged = pr.get('merged', False)
    
    # Determine if this is a merge or regular PR action
    if action == 'closed' and merged:
        event_action = 'MERGE'
    else:
        event_action = 'PULL_REQUEST'
    
    return {
        'request_id': f'PR-{pr_number}',
        'author': author,
        'action': event_action,
        'from_branch': head_branch,
        'to_branch': base_branch,
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    }


@webhook.route('/receiver', methods=["POST"])
def receiver():
    """Receive GitHub webhook events."""
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event_type = request.headers.get('X-GitHub-Event', '')
    payload = request.json
    
    if not payload:
        return jsonify({'error': 'No payload received'}), 400
    
    event_data = None
    
    if event_type == 'push':
        event_data = parse_push_event(payload)
    elif event_type == 'pull_request':
        event_data = parse_pull_request_event(payload)
    elif event_type == 'ping':
        return jsonify({'message': 'Pong! Webhook configured successfully.'}), 200
    else:
        return jsonify({'message': f'Event type {event_type} not handled'}), 200
    
    if event_data:
        # Insert into MongoDB
        result = mongo.db.events.insert_one(event_data)
        event_data['_id'] = str(result.inserted_id)
        return jsonify({'message': 'Event stored successfully', 'event': event_data}), 201
    
    return jsonify({'message': 'No event data to store'}), 200


@webhook.route('/events', methods=['GET'])
def get_events():
    """Get all stored events, sorted by most recent first."""
    events = list(mongo.db.events.find().sort('_id', -1).limit(50))
    
    # Convert ObjectId to string for JSON serialization
    for event in events:
        event['_id'] = str(event['_id'])
    
    return jsonify(events)


@webhook.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now(timezone.utc).isoformat()})
