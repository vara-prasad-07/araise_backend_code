import numpy as np
import time

class CoordinateProcessor:
    """Lightweight processor that works with coordinates instead of video frames"""
    
    @staticmethod
    def calculate_angle(a, b, c):
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    @staticmethod
    def validate_coordinates(coords_dict, required_points):
        """Validate that required coordinate points are present and valid"""
        for point in required_points:
            if point not in coords_dict:
                return False
            coord = coords_dict[point]
            if not coord or len(coord) < 2:
                return False
            if coord[0] is None or coord[1] is None:
                return False
        return True

class BicepCurlCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 50
        self.max_angle_threshold = 140
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for bicep curl
        Expected coordinates format: {
            'right_shoulder': [x, y],
            'right_elbow': [x, y], 
            'right_wrist': [x, y]
        }
        """
        required_points = ['right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates
        shoulder = coordinates['right_shoulder']
        elbow = coordinates['right_elbow']
        wrist = coordinates['right_wrist']
        
        # Calculate and smooth angle
        raw_angle = CoordinateProcessor.calculate_angle(shoulder, elbow, wrist)
        angle = self.smooth_angle(raw_angle)
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Bicep curl logic
        if angle > self.max_angle_threshold:
            if self.stage != "down":
                self.stage = "down"
                current_stage = "down"
            feedback = "Lower your arm more"
            
        elif angle < self.min_angle_threshold and self.stage == "down":
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
                self.counter += 1
                feedback = "Great rep! Lower your arm"
            else:
                feedback = "Hold the curl"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "down":
                feedback = "Keep curling up"
            elif self.stage == "up":
                feedback = "Lower your arm slowly"
            else:
                feedback = "Start with arm extended"
        else:
            feedback = f"Current angle: {int(angle)}°"
        print(self.counter, feedback, int(angle), current_stage or "ready")    
        
        return self.counter, feedback, int(angle), current_stage or "ready"

class SquatCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 70
        self.max_angle_threshold = 160
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for squat
        Expected coordinates format: {
            'right_hip': [x, y],
            'right_knee': [x, y],
            'right_ankle': [x, y]
        }
        """
        required_points = ['right_hip', 'right_knee', 'right_ankle']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates
        hip = coordinates['right_hip']
        knee = coordinates['right_knee']
        ankle = coordinates['right_ankle']
        
        # Calculate and smooth angle
        raw_angle = CoordinateProcessor.calculate_angle(hip, knee, ankle)
        angle = self.smooth_angle(raw_angle)
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Squat logic
        if angle > self.max_angle_threshold:
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
            feedback = "Standing position"
            
        elif angle < self.min_angle_threshold and self.stage == "up":
            if self.stage != "down":
                self.stage = "down"
                current_stage = "down"
                self.counter += 1
                feedback = "Great squat! Stand up"
            else:
                feedback = "Hold the squat"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "up":
                feedback = "Keep squatting down"
            elif self.stage == "down":
                feedback = "Stand up slowly"
            else:
                feedback = "Start standing up"
        else:
            feedback = f"Current angle: {int(angle)}°"
        
        return self.counter, feedback, int(angle), current_stage or "ready"

class PushupCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 70
        self.max_angle_threshold = 160
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for pushup
        Expected coordinates format: {
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates
        shoulder = coordinates['right_shoulder']
        elbow = coordinates['right_elbow']
        wrist = coordinates['right_wrist']
        
        # Calculate and smooth angle
        raw_angle = CoordinateProcessor.calculate_angle(shoulder, elbow, wrist)
        angle = self.smooth_angle(raw_angle)
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Pushup logic
        if angle > self.max_angle_threshold:
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
            feedback = "Plank position"
            
        elif angle < self.min_angle_threshold and self.stage == "up":
            if self.stage != "down":
                self.stage = "down"
                current_stage = "down"
                self.counter += 1
                feedback = "Great pushup! Push back up"
            else:
                feedback = "Hold the bottom position"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "up":
                feedback = "Keep lowering down"
            elif self.stage == "down":
                feedback = "Push back up"
            else:
                feedback = "Start in plank position"
        else:
            feedback = f"Current angle: {int(angle)}°"
        
        return self.counter, feedback, int(angle), current_stage or "ready"

class PlankCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_hip_angle = 160
        self.max_hip_angle = 190
        self.start_time = None
        self.total_time = 0
        self.is_in_plank = False
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for plank
        Expected coordinates format: {
            'right_shoulder': [x, y],
            'right_hip': [x, y],
            'right_knee': [x, y]
        }
        """
        required_points = ['right_shoulder', 'right_hip', 'right_knee']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates
        shoulder = coordinates['right_shoulder']
        hip = coordinates['right_hip']
        knee = coordinates['right_knee']
        
        # Calculate and smooth angle
        raw_angle = CoordinateProcessor.calculate_angle(shoulder, hip, knee)
        angle = self.smooth_angle(raw_angle)
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Plank logic - check if body is straight
        if self.min_hip_angle <= angle <= self.max_hip_angle:
            if not self.is_in_plank:
                self.is_in_plank = True
                self.start_time = time.time()
                self.stage = "holding"
                current_stage = "holding"
                feedback = "Perfect plank! Hold it!"
            else:
                # Update time
                if self.start_time:
                    current_time = time.time()
                    self.counter = int(current_time - self.start_time + self.total_time)
                feedback = f"Great form! Hold for {self.counter}s"
                current_stage = "holding"
                
        else:
            if self.is_in_plank:
                # Was in plank, now out - save the time
                if self.start_time:
                    self.total_time += time.time() - self.start_time
                    self.start_time = None
                self.is_in_plank = False
                
            self.stage = "adjusting"
            current_stage = "adjusting"
            
            if angle < self.min_hip_angle:
                feedback = "Lower your hips - keep body straight"
            elif angle > self.max_hip_angle:
                feedback = "Raise your hips - keep body straight"
            else:
                feedback = "Get into plank position"
        
        return self.counter, feedback, int(angle), current_stage or "ready"
