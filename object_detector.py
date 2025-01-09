import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, min_area=1000):
        self.min_area = min_area

    def preprocess_frame(self, frame):
        """Preprocess frame for object detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        edges = cv2.Canny(blur, 30, 90)
        kernel = np.ones((5, 5))
        dilated = cv2.dilate(edges, kernel, iterations=2)
        return dilated

    def detect_objects(self, frame):
        """Detect objects in frame using contour detection"""
        processed = self.preprocess_frame(frame)
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects = []
        
        # Remove debug window display to prevent interference
        # debug_frame = frame.copy()
        # cv2.drawContours(debug_frame, contours, -1, (0, 255, 0), 2)
        # cv2.imshow('All Contours', debug_frame)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.min_area:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int32(box)
                objects.append((box, rect))
        
        return objects