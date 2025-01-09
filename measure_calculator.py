class MeasurementCalculator:
    def __init__(self):
        self.pixels_per_cm = None
        
    def calibrate(self, pixel_width, reference_width_cm):
        """Calibrate using reference object"""
        self.pixels_per_cm = pixel_width / reference_width_cm
        return self.pixels_per_cm
        
    def calculate_dimensions(self, objects):
        """Calculate real-world dimensions of detected objects"""
        if self.pixels_per_cm is None:
            return []
            
        measurements = []
        for box, rect in objects:
            width = rect[1][0]  # pixels
            height = rect[1][1]  # pixels
            
            real_width = width / self.pixels_per_cm
            real_height = height / self.pixels_per_cm
            measurements.append((box, real_width, real_height))
        
        return measurements