import cv2
import numpy as np

class ColorDetector:
    def __init__(self):
        # Pre-defined color ranges for blue marker
        self.lower_blue = np.array([100, 60, 60])
        self.upper_blue = np.array([140, 255, 255])
        
    def detect_color(self, frame):
        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for blue color
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        
        # Remove noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        return mask
