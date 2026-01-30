# GitHub Webhook Monitor - React Frontend

A React application that polls the Flask backend every 15 seconds and displays GitHub webhook events.

## 🚀 Features

- Real-time polling (every 15 seconds)
- Displays PUSH, PULL_REQUEST, and MERGE events
- Dark mode GitHub-inspired design
- Countdown timer showing next refresh

## 📋 Prerequisites

- Node.js 18+
- Deployed Flask backend URL

## 🛠️ Local Development

```bash
# Install dependencies
npm install

# Create .env file with your backend URL
echo "VITE_API_URL=http://localhost:5000" > .env

# Run development server
npm run dev
```

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. Push this folder to a GitHub repository
2. Go to [vercel.com](https://vercel.com) and import your repository
3. Set the **Root Directory** to `frontend` (if in a monorepo)
4. Add environment variable:
   - `VITE_API_URL` = `https://your-flask-backend-url.com`
5. Deploy!

### Deploy to Netlify

1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify
3. Set environment variable `VITE_API_URL`

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Flask backend URL | `https://webhook-backend.onrender.com` |

## 📊 Event Display Formats

- **PUSH**: `{author} pushed to {to_branch} on {timestamp}`
- **PULL_REQUEST**: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **MERGE**: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`
