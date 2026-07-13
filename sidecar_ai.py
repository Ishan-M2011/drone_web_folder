import cv2
import socketio
import base64
import numpy as np
from ultralytics import YOLO

sio = socketio.Client()
# Connect to your live Render server
sio.connect("https://drone-stream-server.onrender.com")

model = YOLO("yolov8n.pt")

@sio.on('raw_frame')
def on_frame(data):
    # 1. Decode the raw frame from the Pi
    nparr = np.frombuffer(base64.b64decode(data['image']), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2. Run AI and draw boxes
    results = model(frame)
    annotated_frame = results[0].plot()

    # 3. Send the finished frame back to the server to be shown on website
    _, buffer = cv2.imencode('.jpg', annotated_frame)
    b64_frame = base64.b64encode(buffer).decode('utf-8')
    sio.emit('processed_frame', {'image': b64_frame})

print("Sidecar AI ready and waiting for frames...")
sio.wait()