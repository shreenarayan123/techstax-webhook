import { useState, useEffect, useCallback } from 'react'

const POLL_INTERVAL = 15000 // 15 seconds
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

function App() {
    const [events, setEvents] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [countdown, setCountdown] = useState(15)
    const [lastUpdated, setLastUpdated] = useState(null)

    const fetchEvents = useCallback(async () => {
        try {
            const response = await fetch(`${API_URL}/webhook/events`)
            if (!response.ok) {
                throw new Error('Failed to fetch events')
            }
            const data = await response.json()
            setEvents(data)
            setError(null)
            setLastUpdated(new Date())
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }, [])

    // Initial fetch and polling
    useEffect(() => {
        fetchEvents()

        const pollInterval = setInterval(() => {
            fetchEvents()
            setCountdown(15)
        }, POLL_INTERVAL)

        return () => clearInterval(pollInterval)
    }, [fetchEvents])

    // Countdown timer
    useEffect(() => {
        const countdownInterval = setInterval(() => {
            setCountdown(prev => (prev > 0 ? prev - 1 : 15))
        }, 1000)

        return () => clearInterval(countdownInterval)
    }, [])

    const formatEventMessage = (event) => {
        const { author, action, from_branch, to_branch, timestamp } = event

        switch (action) {
            case 'PUSH':
                return (
                    <>
                        <span className="author">{author}</span> pushed to{' '}
                        <span className="branch">{to_branch}</span> on{' '}
                        <span className="timestamp">{timestamp}</span>
                    </>
                )
            case 'PULL_REQUEST':
                return (
                    <>
                        <span className="author">{author}</span> submitted a pull request from{' '}
                        <span className="branch">{from_branch}</span> to{' '}
                        <span className="branch">{to_branch}</span> on{' '}
                        <span className="timestamp">{timestamp}</span>
                    </>
                )
            case 'MERGE':
                return (
                    <>
                        <span className="author">{author}</span> merged branch{' '}
                        <span className="branch">{from_branch}</span> to{' '}
                        <span className="branch">{to_branch}</span> on{' '}
                        <span className="timestamp">{timestamp}</span>
                    </>
                )
            default:
                return `${author} performed ${action} on ${timestamp}`
        }
    }

    return (
        <div className="app">
            <header className="header">
                <h1>🔗 GitHub Webhook Monitor</h1>
                <p>Real-time tracking of repository events</p>
            </header>

            <div className="status-bar">
                <div className="status-indicator"></div>
                <span className="status-text">
                    Auto-refresh in <span className="countdown">{countdown}s</span>
                </span>
                {lastUpdated && (
                    <span className="status-text">
                        | Last updated: {lastUpdated.toLocaleTimeString()}
                    </span>
                )}
            </div>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <span>Loading events...</span>
                </div>
            )}

            {error && (
                <div className="error">
                    ⚠️ Error: {error}. Make sure the Flask server is running.
                </div>
            )}

            {!loading && !error && events.length === 0 && (
                <div className="empty-state">
                    <div className="empty-state-icon">📭</div>
                    <h3>No events yet</h3>
                    <p>
                        Push some code, open a pull request, or merge a branch in your
                        action-repo to see events appear here.
                    </p>
                </div>
            )}

            <div className="events-container">
                {events.map((event) => (
                    <div
                        key={event._id}
                        className={`event-card ${event.action.toLowerCase()}`}
                    >
                        <div className="event-header">
                            <span className={`event-badge ${event.action.toLowerCase()}`}>
                                {event.action.replace('_', ' ')}
                            </span>
                            <span className="event-id">{event.request_id}</span>
                        </div>
                        <div className="event-message">
                            {formatEventMessage(event)}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default App
