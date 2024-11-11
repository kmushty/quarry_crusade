import os
from flask import Flask, send_from_directory
from app import create_app, socketio
from flask_cors import CORS

app = create_app()
CORS(app)

# Serve React's static files in production
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.root_path, 'frontend/build'), path)

# Serve the index.html for React
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'frontend/build'), 'index.html')

if __name__ == "__main__":
    # Run the app with SocketIO support and React
    socketio.run(app, host="127.0.0.1", port=3001, debug=True)
