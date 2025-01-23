import cv2
import numpy as np
from picamera2 import Picamera2
from datetime import datetime
import json
import os

from object_detector import ObjectDetector
from measure_calculator import MeasurementCalculator
from distance_calculator import DistanceCalculator
from visualization import Visualizer

class ObjectMeasurement:
    def __init__(self):
        # Create data directory
        self.data_dir = os.path.join(os.path.expanduser('~'), 'application/data')
        os.makedirs(self.data_dir, exist_ok=True)

        print("Initializing camera...")
        try:
            self.picam2 = Picamera2()
            preview_config = self.picam2.create_preview_configuration()
            preview_config["main"]["size"] = (640, 480)
            self.picam2.configure(preview_config)
            self.picam2.start()
            print("Camera initialized successfully")
            
        except Exception as e:
            raise Exception(f"Could not initialize camera: {e}")
            
        self.detector = ObjectDetector(min_area=1000)
        self.calculator = MeasurementCalculator()
        self.distance_calculator = DistanceCalculator()
        self.visualizer = Visualizer()
        
        self.reference_object_width = 8.56  # Credit card width in cm
        self.calibrated = False
        self.measurement_threshold = 20  # cm
        print("Initialization complete")

    def save_measurement(self, measurement):
        """Save measurement to JSON file"""
        filename = f"{self.data_dir}/measurement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(measurement, f)

    def calibrate(self, frame):
        """Calibrate using reference object"""
        try:
            print("Starting calibration process...")
            objects = self.detector.detect_objects(frame)
            if objects:
                box, rect = objects[0]
                width_pixels = max(rect[1])  # Get the larger dimension
                
                self.calculator.calibrate(width_pixels, self.reference_object_width)
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
                    width_cm, length_cm = dimensions[0][1:3]
                    
                    # Print measurements
                    print(f"\nMeasurement:")
                    print(f"Width: {width_cm:.2f} cm")
                    print(f"Length: {length_cm:.2f} cm")
                    print(f"Distance: {distance:.2f} cm")
                    
                    # Store measurement data
                    measurement = {
                        'timestamp': datetime.now().isoformat(),
                        'width_cm': round(width_cm, 2),
                        'length_cm': round(length_cm, 2),
                        'distance_cm': round(distance, 2)
                    }
                    
                    # Save measurement
                    self.save_measurement(measurement)
                    
                    measurements.append((box, width_cm, length_cm, distance))
        
        self.visualizer.draw_measurements_with_distance(frame, measurements)

    def run(self):
        print("Starting main loop...")
        while True:
            frame = self.picam2.capture_array()
            
            # Convert frame to BGR format for OpenCV processing
            if frame.shape[-1] == 3:  # If RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if not self.calibrated:
                # Assuming Visualizer has a method to draw calibration info
                cv2.putText(frame, "Place credit card at 30cm and press 'c' to calibrate",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
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
        self.picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        print("Starting application...")
        measurer = ObjectMeasurement()
        measurer.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        cv2.destroyAllWindows()