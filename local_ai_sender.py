import cv2
import socketio
import base64
import numpy as np
from ultralytics import YOLO

sio = socketio.Client()
# REPLACE with your actual Render URL
sio.connect("https://drone-stream-server.onrender.com")

model = YOLO("yolov8n.pt")

@sio.on('video_frame')
def on_frame(data):
    # Decode raw frame from Pi
    nparr = np.frombuffer(base64.b64decode(data['image']), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run AI
    results = model(frame)
    annotated_frame = results[0].plot()

    # Show the perfect window
    cv2.imshow("Remote AI Mission Control", annotated_frame)
    cv2.waitKey(1)

    # Push processed frame to web
    _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    b64_frame = base64.b64encode(buffer).decode('utf-8')
    sio.emit('processed_feed', {'image': b64_frame})

print("Brain active. Waiting for drone feed...")
sio.wait()