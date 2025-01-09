import cv2
import numpy as np
from object_detector import ObjectDetector
from measure_calculator import MeasurementCalculator
from distance_calculator import DistanceCalculator
from visualization import Visualizer

class ObjectMeasurement:
    def __init__(self):
        print("Initializing camera...")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1920)  # width
        self.cap.set(4, 1080)  # height
        
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
            
        self.detector = ObjectDetector(min_area=1000)
        self.calculator = MeasurementCalculator()
        self.distance_calculator = DistanceCalculator()
        self.visualizer = Visualizer()
        
        self.reference_object_width = 8.56  # Credit card width in cm
        self.calibrated = False
        self.measurement_threshold = 20  # cm - only measure objects closer than this
        print("Initialization complete")

    def calibrate(self, frame):
        """Calibrate using reference object"""
        try:
            print("Starting calibration process...")
            objects = self.detector.detect_objects(frame)
            if objects:
                # Use largest object for calibration
                box, rect = objects[0]
                width_pixels = max(rect[1])  # Get the larger dimension
                self.calculator.calibrate(width_pixels, self.reference_object_width)
                # Calibrate distance calculator (assuming credit card is at 30cm during calibration)
                self.distance_calculator.calibrate(width_pixels, distance_cm=30)
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                print(f"Found calibration object with width: {width_pixels} pixels")
                return True
            print("No suitable calibration object found")
            return False
        except Exception as e:
            print(f"Calibration error: {e}")
            return False

    def process_frame(self, frame):
        """Process a single frame"""
        objects = self.detector.detect_objects(frame)
        measurements = []
        
        for box, rect in objects:
            width_pixels = max(rect[1])  # Get the larger dimension
            distance = self.distance_calculator.calculate_distance(width_pixels)
            
            # Only measure objects within threshold distance
            if distance is not None and distance <= self.measurement_threshold:
                dimensions = self.calculator.calculate_dimensions([(box, rect)])
                if dimensions:
                    measurements.append((box, *dimensions[0][1:], distance))
        
        self.visualizer.draw_measurements_with_distance(frame, measurements)

    def run(self):
        print("Starting main loop...")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            if not self.calibrated:
                self.visualizer.draw_calibration_info(frame, False)
            else:
                self.process_frame(frame)
            
            cv2.imshow('Object Measurement', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('c') and not self.calibrated:
                print("Attempting calibration...")
                self.calibrated = self.calibrate(frame)
                if self.calibrated:
                    print("Calibration successful!")
                else:
                    print("Calibration failed. Please try again.")

        print("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        print("Starting application...")
        measurer = ObjectMeasurement()
        measurer.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        cv2.destroyAllWindows()