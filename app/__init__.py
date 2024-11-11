# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from .config import Config

mongo = PyMongo()     # Initialize PyMongo
socketio = SocketIO() # Initialize SocketIO

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize SocketIO for WebSockets
    socketio.init_app(app, cors_allowed_origins="*")
    print("SocketIO initialized")

    # Register blueprints for modular routes (this basically handles the routing of messages between vehicles and the webapp)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print("Main blueprint registered")

    return app

