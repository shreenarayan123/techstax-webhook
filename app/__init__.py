from flask import Flask
from flask_cors import CORS
import os

from app.webhook.routes import webhook
from app.extensions import mongo, MONGO_URI


# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # Enable CORS for React frontend
    CORS(app)
    
    # Configure MongoDB
    app.config["MONGO_URI"] = MONGO_URI
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
