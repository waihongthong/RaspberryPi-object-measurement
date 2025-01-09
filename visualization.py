import cv2
import numpy as np

class Visualizer:
    @staticmethod
    def draw_measurements_with_distance(frame, measurements):
        """Draw boxes, measurements, and distance on frame"""
        for box, width, height, distance in measurements:
            # Draw contour
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
            
            # Calculate center point
            center_x = np.mean(box[:, 0])
            center_y = np.mean(box[:, 1])
            
            # Draw measurements
            dimensions_text = f'{width:.1f}cm x {height:.1f}cm'
            distance_text = f'Distance: {distance:.1f}cm'
            
            # Draw text with slight offset to avoid overlap
            cv2.putText(frame, dimensions_text,
                       (int(center_x) - 50, int(center_y)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(frame, distance_text,
                       (int(center_x) - 50, int(center_y) + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    @staticmethod
    def draw_calibration_info(frame, calibrated):
        """Draw calibration status and instructions"""
        if not calibrated:
            cv2.putText(frame, "Place reference object (credit card) at 30cm and press 'c' to calibrate",
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Calibrated - Measuring Objects within 20cm",
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)