import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# The secret key secures the websocket session
app.config['SECRET_KEY'] = 'drone_secret_key_123!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # Serves the HTML webpage when someone visits the URL
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(data):
    # Simply forward the base64 string directly out to all web clients
    emit('response_back', {'image': data['image']}, broadcast=True)

if __name__ == '__main__':
    # Cloud hosts specify a dynamic PORT variable we must listen to
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)