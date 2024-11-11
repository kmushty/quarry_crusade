# run.py
from app import create_app, socketio

app = create_app()

# Add a test route for "/"
@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    # run on loopback for now?
    socketio.run(app, host="127.0.0.1", port=3000, debug=True)

