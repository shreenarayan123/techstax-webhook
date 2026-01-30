from flask_pymongo import PyMongo
import os

# Setup MongoDB here
mongo = PyMongo()

# MongoDB URI - can be overridden by environment variable
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/github_webhooks')
