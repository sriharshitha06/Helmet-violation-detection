import cv2
import easyocr
import numpy as np

class ANPR:
    def __init__(self, languages=['en'], gpu=False):
        """
        Initialize the ANPR system.
        :param languages: List of languages for OCR.
        :param gpu: Boolean to use GPU.
        """
        self.reader = easyocr.Reader(languages, gpu=gpu)

    def extract_license_plate(self, frame, detection_box):
        """
        Crop the license plate from the frame.
        :param frame: Full image frame.
        :param detection_box: Bounding box [x1, y1, x2, y2].
        :return: Cropped image of the license plate.
        """
        x1, y1, x2, y2 = map(int, detection_box)
        # Add some padding if possible
        h, w = frame.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        cropped_plate = frame[y1:y2, x1:x2]
        return cropped_plate

    def recognize_text(self, plate_image):
        """
        Perform OCR on the license plate image.
        :param plate_image: Cropped image of the license plate.
        :return: Detected text and confidence.
        """
        if plate_image is None or plate_image.size == 0:
            return "", 0.0

        # Preprocessing for better OCR
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        # Simple thresholding or other preprocessing can be added here
        
        results = self.reader.readtext(gray)
        
        # Filter and concatenate results
        text = ""
        confidence = 0.0
        
        if results:
            # Sort by confidence or position? Usually just take the most confident or concat
            # format: ([[x,y]...], 'text', conf)
            best_result = max(results, key=lambda x: x[2])
            text = best_result[1]
            confidence = best_result[2]
            
            # Basic validation: alphanumeric only, remove spaces
            text = ''.join(e for e in text if e.isalnum())
            
        return text, confidence
