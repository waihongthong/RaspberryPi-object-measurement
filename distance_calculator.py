import numpy as np

class DistanceCalculator:
    def __init__(self, reference_width_cm=8.56):  # Credit card width
        self.reference_width_cm = reference_width_cm
        self.focal_length = None
        
    def calibrate(self, perceived_width_pixels, distance_cm=30):
        """
        Calibrate using reference object at known distance
        Using the formula: F = (P × D) / W
        where:
        F is focal length
        P is perceived width in pixels
        D is known distance in cm
        W is known width in cm
        """
        self.focal_length = (perceived_width_pixels * distance_cm) / self.reference_width_cm
        return self.focal_length
        
    def calculate_distance(self, perceived_width_pixels):
        """
        Calculate distance to object using the formula: D = (W × F) / P
        Returns distance in cm
        """
        if self.focal_length is None:
            return None
            
        distance = (self.reference_width_cm * self.focal_length) / perceived_width_pixels
        return distance