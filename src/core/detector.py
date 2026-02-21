from ultralytics import YOLO
import cv2
import math

class HelmetDetector:
    def __init__(self, model_path, conf_thres=0.5):
        """
        Initialize the YOLO detector.
        :param model_path: Path to the trained YOLO weights.
        :param conf_thres: Confidence threshold for detection.
        """
        self.model = YOLO(model_path)
        self.conf_thres = conf_thres
        # Mock class names if using standard YOLOv8n (person, motorcycle)
        # In a real scenario, this should match the custom model classes
        # e.g., {0: 'rider', 1: 'helmet', 2: 'no_helmet', 3: 'license_plate'}
        self.classes = self.model.names 

    def detect(self, frame):
        """
        Run inference on a frame.
        :param frame: Input image frame.
        :return: List of detections.
        """
        results = self.model(frame, conf=self.conf_thres, verbose=False)
        return results

    def plot_results(self, frame, results):
        """
        Draw bounding boxes on the frame.
        """
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # Confidence
                conf = math.ceil((box.conf[0]*100))/100
                
                # Class Name
                cls = int(box.cls[0])
                current_class = self.classes[cls]

                # Color based on class
                if current_class == 'no_helmet':
                    color = (0, 0, 255) # Red for violation
                elif current_class == 'helmet':
                    color = (0, 255, 0) # Green for compliant
                else: 
                    color = (255, 0, 0) # Blue for others

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                cv2.putText(frame, f'{current_class} {conf}', (max(0, x1), max(35, y1)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame
