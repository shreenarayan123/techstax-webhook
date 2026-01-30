# Webhook Receiver - Flask Backend

A Flask API that receives GitHub webhook events and stores them in MongoDB.

## 🚀 Features

- Webhook endpoint for GitHub events
- Parses PUSH, PULL_REQUEST, and MERGE events  
- Stores events in MongoDB
- REST API to fetch stored events

## 📋 Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB)

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI

# Run the server
python run.py
```

## 🚀 Deployment to Render

1. Push this repository to GitHub
2. Go to [render.com](https://render.com)
3. Create a new **Web Service**
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
6. Add environment variable:
   - `MONGO_URI` = `mongodb+srv://...your-atlas-connection-string...`
7. Deploy!

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook/receiver` | POST | Receives GitHub webhook events |
| `/webhook/events` | GET | Returns stored events (latest 50) |
| `/webhook/health` | GET | Health check endpoint |

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGO_URI` | MongoDB connection string | Yes |
| `WEBHOOK_SECRET` | GitHub webhook secret | No |
| `PORT` | Server port | No (default: 5000) |

## 📊 MongoDB Schema

```javascript
{
  _id: ObjectId,
  request_id: String,    // Commit hash or PR ID
  author: String,        // GitHub username
  action: String,        // "PUSH" | "PULL_REQUEST" | "MERGE"
  from_branch: String,   // Source branch
  to_branch: String,     // Target branch
  timestamp: String      // UTC datetime
}
```