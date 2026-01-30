# Webhook Repo - GitHub Webhook Receiver

A Flask application that receives GitHub webhook events (Push, Pull Request, Merge) and stores them in MongoDB. Includes a React frontend that polls for new events every 15 seconds.

## 🚀 Features

- 📥 Receives GitHub webhook events (Push, Pull Request, Merge)
- 💾 Stores events in MongoDB with proper schema
- 🔄 React UI with 15-second auto-polling
- 🎨 Modern dark theme inspired by GitHub
- 🔐 Optional webhook signature verification

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB (local or Atlas)

## 🛠️ Setup

### 1. Backend Setup

```bash
# Navigate to webhook folder
cd webhook

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env
# Edit .env with your MongoDB connection string

# Run the Flask server
python run.py
```

The server will start at `http://localhost:5000`

### 2. Frontend Setup

```bash
cd webhook/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will start at `http://localhost:3000`

### 3. Configure GitHub Webhook

1. Go to your `action-repo` on GitHub → **Settings** → **Webhooks**
2. Click **"Add webhook"**
3. Configure:
   - **Payload URL**: `https://your-server.com/webhook/receiver` (use ngrok for local testing)
   - **Content type**: `application/json`
   - **Secret**: (optional) Same as `WEBHOOK_SECRET` in .env
   - **Events**: Select **"Let me select individual events"**
     - ✅ Pushes
     - ✅ Pull requests
4. Click **"Add webhook"**

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook/receiver` | POST | Receives GitHub webhook events |
| `/webhook/events` | GET | Returns stored events (latest 50) |
| `/webhook/health` | GET | Health check endpoint |

## 📊 Event Display Formats

The UI displays events in these formats:

- **PUSH**: `{author} pushed to {to_branch} on {timestamp}`
- **PULL_REQUEST**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **MERGE**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

## 🗄️ MongoDB Schema

```javascript
{
  _id: ObjectId,           // MongoDB default
  request_id: String,      // Commit hash or PR ID
  author: String,          // GitHub username
  action: String,          // "PUSH" | "PULL_REQUEST" | "MERGE"
  from_branch: String,     // Source branch
  to_branch: String,       // Target branch
  timestamp: String        // UTC datetime string
}
```

## 🧪 Testing with ngrok

For local testing with real GitHub webhooks:

```bash
# Start ngrok
ngrok http 5000

# Use the ngrok URL as your webhook Payload URL
# Example: https://abc123.ngrok.io/webhook/receiver
```

## 📁 Project Structure

```
webhook/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── extensions.py        # MongoDB setup
│   └── webhook/
│       ├── __init__.py
│       └── routes.py        # Webhook endpoints
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── index.css        # Styles
│   │   └── main.jsx         # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── run.py                   # Flask runner
├── requirements.txt
├── .env.example
└── README.md
```