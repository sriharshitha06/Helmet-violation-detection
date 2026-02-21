from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import time
import os
import sys

# Add project root to path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.core.camera import VideoStream
from src.core.detector import HelmetDetector
from src.core.anpr import ANPR
from src.database import DatabaseManager

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize components
# NOTE: Using a placeholder model path. User needs to replace with actual model.
# If 'yolov8n.pt' is used, logic needs to be adapted as it detects generic classes.
# We will check if 'helmet_yolov8.pt' exists, else use standard 'yolov8n.pt'
MODEL_PATH = os.path.join('models', 'helmet_yolov8.pt') 
if not os.path.exists(MODEL_PATH):
    print(f"Warning: {MODEL_PATH} not found. Downloading/Using 'yolov8n.pt' for demo.")
    MODEL_PATH = 'yolov8n.pt'

detector = HelmetDetector(MODEL_PATH)
anpr = ANPR(gpu=False) # Set to True if GPU is available
db_manager = DatabaseManager(db_path='sqlite:///data/violations.db')
camera = VideoStream(src=0).start() # Default to webcam

# Global specific to latest frame for streaming
outputFrame = None
lock = threading.Lock()

def process_stream():
    global outputFrame, lock
    
    # Simple logic to prevent flooding DB with same violation
    last_violation_time = 0
    cooldown = 5 # seconds

    while True:
        frame = camera.read()
        if frame is None:
            continue

        # Resize for performance detection
        frame_resized = cv2.resize(frame, (640, 480))
        results = detector.detect(frame_resized)
        
        # Detection Loop
        # Needs simplified logic: if 'motorcycle' and 'rider' and 'no_helmet' detected
        # For Demo with standard YOLO: if 'person' and 'motorcycle' are overlapping
        
        # Draw results
        frame_processed = detector.plot_results(frame_resized.copy(), results)
        
        # Logic for Violation Trigger
        # This is a critical part that depends on the model's classes.
        # Assuming the model returns 'no_helmet' class.
        
        violation_detected = False
        plate_text = "Unknown"
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = detector.classes[cls_id]
                
                if cls_name == 'no_helmet':
                    violation_detected = True
                    # In a real app, we'd associate this with a motorcycle
                    pass

        if violation_detected and (time.time() - last_violation_time > cooldown):
            # Attempt ANPR
            # For simplicity, we scan the whole frame or a ROI if we had bike box
            # Ideally, pass the ROI of the bike to ANPR
            # Here we just try to find ANY text in the frame (simplified)
            # OR better: if we have a 'license_plate' class in YOLO, we crop that.
            
            # Simulated ANPR for now if no specific plate box
            # If standard YOLO matches 'truck' or 'car' or 'motorcycle', we can crop that region
            
            # Capture Evidence
            timestamp = int(time.time())
            filename = f"violation_{timestamp}.jpg"
            filepath = os.path.join("data", "evidence", filename)
            
            # Save original frame
            cv2.imwrite(filepath, frame)
            
            db_manager.add_violation(plate_text, filepath)
            last_violation_time = time.time()
            print(f"Violation Detected! Saved to {filepath}")

        with lock:
            outputFrame = frame_processed.copy()

def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/api/violations")
def get_violations():
    violations = db_manager.get_violations()
    return jsonify(violations)

if __name__ == "__main__":
    # Start the processing thread
    t = threading.Thread(target=process_stream)
    t.daemon = True
    t.start()
    
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

