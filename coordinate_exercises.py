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

class BenchPressCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Bottom position (elbows bent)
        self.max_angle_threshold = 160  # Top position (arms extended)
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for bench press exercise
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'right_shoulder', 'right_elbow']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        
        # Calculate angles for both arms
        # For left arm: shoulder -> elbow -> virtual point extending from elbow
        left_dx = left_elbow[0] - left_shoulder[0]
        left_dy = left_elbow[1] - left_shoulder[1]
        left_virtual_wrist = [left_elbow[0] + left_dx, left_elbow[1] + left_dy]
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_virtual_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        # For right arm: shoulder -> elbow -> virtual point extending from elbow
        right_dx = right_elbow[0] - right_shoulder[0]
        right_dy = right_elbow[1] - right_shoulder[1]
        right_virtual_wrist = [right_elbow[0] + right_dx, right_elbow[1] + right_dy]
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_virtual_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Bench press logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
            feedback = "Arms fully extended - good!"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "up":
            self.stage = "down"
            current_stage = "down"
            self.counter += 1
            feedback = f"Rep {self.counter} completed! Press back up"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "up":
                feedback = "Lower the weight slowly"
            elif self.stage == "down":
                feedback = "Press the weight up"
            else:
                feedback = "Start with arms extended"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"
class RopePulldownCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 60   # Arms fully brought together (contraction)
        self.max_angle_threshold = 150  # Arms open (start position)
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for rope pulldown (cable crossover)
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
        
        # Rope pulldown / cable fly logic
        if angle > self.max_angle_threshold:
            if self.stage != "open":
                self.stage = "open"
                current_stage = "open"
            feedback = "Arms open - starting position"
            
        elif angle < self.min_angle_threshold and self.stage == "open":
            if self.stage != "close":
                self.stage = "close"
                current_stage = "close"
                self.counter += 1
                feedback = "Good contraction! Return slowly"
            else:
                feedback = "Hold contraction"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "open":
                feedback = "Bring arms together"
            elif self.stage == "close":
                feedback = "Control back to start"
            else:
                feedback = "Start with arms open"
        else:
            feedback = f"Current angle: {int(angle)}°"
        
        return self.counter, feedback, int(angle), current_stage or "ready"

class BentTricepPullCoordinates:
    def __init__(self):
        
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 90   # Start (elbow bent)
        self.max_angle_threshold = 160  # End (arm fully extended)
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for bent tricep pull
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
        
        # Tricep pull logic
        if angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Arm fully extended"
            
        elif angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "bent":
                self.stage = "bent"
                current_stage = "bent"
                self.counter += 1
                feedback = "Good rep! Extend again"
            else:
                feedback = "Hold bent position"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Slowly bend elbow"
            elif self.stage == "bent":
                feedback = "Push cable down"
            else:
                feedback = "Start with elbow slightly bent"
        else:
            feedback = f"Current angle: {int(angle)}°"
        
        return self.counter, feedback, int(angle), current_stage or "ready"


class CrunchCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer = []
        self.min_angle_threshold = 80   # Crunch position (torso bent forward)
        self.max_angle_threshold = 160  # Upright position
        
    def smooth_angle(self, angle, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        self.angle_buffer.append(angle)
        if len(self.angle_buffer) > buffer_size:
            self.angle_buffer.pop(0)
        return sum(self.angle_buffer) / len(self.angle_buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for kneeling cable crunch
        Expected coordinates format: {
            'right_knee': [x, y],
            'right_hip': [x, y],
            'right_shoulder': [x, y]
        }
        """
        required_points = ['right_knee', 'right_hip', 'right_shoulder']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates
        knee = coordinates['right_knee']
        hip = coordinates['right_hip']
        shoulder = coordinates['right_shoulder']
        
        # Calculate and smooth torso angle
        raw_angle = CoordinateProcessor.calculate_angle(knee, hip, shoulder)
        angle = self.smooth_angle(raw_angle)
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Crunch logic
        if angle > self.max_angle_threshold:
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
            feedback = "Torso upright - start position"
            
        elif angle < self.min_angle_threshold and self.stage == "up":
            if self.stage != "down":
                self.stage = "down"
                current_stage = "down"
                self.counter += 1
                feedback = "Good crunch! Return slowly"
            else:
                feedback = "Hold crunch position"
                
        elif self.min_angle_threshold <= angle <= self.max_angle_threshold:
            if self.stage == "up":
                feedback = "Bend forward"
            elif self.stage == "down":
                feedback = "Return to upright"
            else:
                feedback = "Start in upright position"
        else:
            feedback = f"Current angle: {int(angle)}°"
        
        return self.counter, feedback, int(angle), current_stage or "ready"

class PullupCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Arms bent (pulled up position)
        self.max_angle_threshold = 160  # Arms extended (hanging position)
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for pullup exercise
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'left_wrist': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'left_wrist', 
                          'right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        left_wrist = coordinates['left_wrist']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        right_wrist = coordinates['right_wrist']
        
        # Calculate angles for both arms (elbow angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Pullup logic - opposite to pushup (start hanging, pull up)
        if avg_angle > self.max_angle_threshold:
            if self.stage != "hanging":
                self.stage = "hanging"
                current_stage = "hanging"
            feedback = "Hanging position - ready to pull up"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "hanging":
            if self.stage != "up":
                self.stage = "up"
                current_stage = "up"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Lower down slowly"
            else:
                feedback = "Hold the top position"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "hanging":
                feedback = "Pull yourself up"
            elif self.stage == "up":
                feedback = "Lower down slowly"
            else:
                feedback = "Start by hanging from the bar"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"

class ChestSupportedRowCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 60   # Elbows pulled back (contracted position)
        self.max_angle_threshold = 150  # Arms extended (start position)
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for chest supported rows
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'left_wrist': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'left_wrist', 
                          'right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        left_wrist = coordinates['left_wrist']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        right_wrist = coordinates['right_wrist']
        
        # Calculate angles for both arms (elbow angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Chest supported row logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Arms extended - starting position"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "pulled":
                self.stage = "pulled"
                current_stage = "pulled"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Extend arms slowly"
            else:
                feedback = "Hold the pulled position"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Pull elbows back"
            elif self.stage == "pulled":
                feedback = "Extend arms slowly"
            else:
                feedback = "Start with arms extended"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"

class WideGripPulldownCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Arms pulled down (contracted position)
        self.max_angle_threshold = 160  # Arms extended overhead (start position)
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for wide grip pulldown exercise
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'left_wrist': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'left_wrist', 
                          'right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        left_wrist = coordinates['left_wrist']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        right_wrist = coordinates['right_wrist']
        
        # Calculate angles for both arms (elbow angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Wide grip pulldown logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Arms extended overhead - starting position"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "pulled":
                self.stage = "pulled"
                current_stage = "pulled"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Release slowly"
            else:
                feedback = "Hold the pulled position"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Pull the bar down to chest"
            elif self.stage == "pulled":
                feedback = "Release bar slowly"
            else:
                feedback = "Start with arms extended overhead"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"

class LegPressCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Legs bent (knees close to chest)
        self.max_angle_threshold = 160  # Legs extended (pushed out)
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for leg press exercise
        Expected coordinates format: {
            'left_hip': [x, y],
            'left_knee': [x, y],
            'left_ankle': [x, y],
            'right_hip': [x, y],
            'right_knee': [x, y],
            'right_ankle': [x, y]
        }
        """
        required_points = ['left_hip', 'left_knee', 'left_ankle', 
                          'right_hip', 'right_knee', 'right_ankle']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both legs
        left_hip = coordinates['left_hip']
        left_knee = coordinates['left_knee']
        left_ankle = coordinates['left_ankle']
        right_hip = coordinates['right_hip']
        right_knee = coordinates['right_knee']
        right_ankle = coordinates['right_ankle']
        
        # Calculate angles for both legs (knee angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_hip, left_knee, left_ankle)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_hip, right_knee, right_ankle)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both legs for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Leg press logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Legs fully extended - good push!"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "bent":
                self.stage = "bent"
                current_stage = "bent"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Push back out"
            else:
                feedback = "Hold the bent position"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Lower the weight slowly"
            elif self.stage == "bent":
                feedback = "Push the weight out"
            else:
                feedback = "Start with legs extended"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"

class ChestSupportedShoulderPressCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Arms bent (weights at shoulder level)
        self.max_angle_threshold = 160  # Arms extended overhead
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for chest supported shoulder press exercise
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'left_wrist': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'left_wrist', 
                          'right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        left_wrist = coordinates['left_wrist']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        right_wrist = coordinates['right_wrist']
        
        # Calculate angles for both arms (elbow angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Chest supported shoulder press logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Arms fully extended overhead - good press!"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "bent":
                self.stage = "bent"
                current_stage = "bent"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Press back up"
            else:
                feedback = "Hold the bottom position"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Lower the weights slowly"
            elif self.stage == "bent":
                feedback = "Press the weights overhead"
            else:
                feedback = "Start with weights at shoulder level"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"

class OverheadShoulderPressCoordinates:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.angle_buffer_left = []
        self.angle_buffer_right = []
        self.min_angle_threshold = 70   # Arms bent (dumbbells at shoulder level)
        self.max_angle_threshold = 160  # Arms extended overhead
        
    def smooth_angle(self, angle, buffer, buffer_size=5):
        """Smooth angle measurements using a rolling average"""
        buffer.append(angle)
        if len(buffer) > buffer_size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def process_coordinates(self, coordinates):
        """
        Process coordinates for overhead shoulder press exercise
        Expected coordinates format: {
            'left_shoulder': [x, y],
            'left_elbow': [x, y],
            'left_wrist': [x, y],
            'right_shoulder': [x, y],
            'right_elbow': [x, y],
            'right_wrist': [x, y]
        }
        """
        required_points = ['left_shoulder', 'left_elbow', 'left_wrist', 
                          'right_shoulder', 'right_elbow', 'right_wrist']
        
        if not CoordinateProcessor.validate_coordinates(coordinates, required_points):
            return self.counter, "Position yourself properly", 0, "ready"
        
        # Get coordinates for both arms
        left_shoulder = coordinates['left_shoulder']
        left_elbow = coordinates['left_elbow']
        left_wrist = coordinates['left_wrist']
        right_shoulder = coordinates['right_shoulder']
        right_elbow = coordinates['right_elbow']
        right_wrist = coordinates['right_wrist']
        
        # Calculate angles for both arms (elbow angles)
        left_raw_angle = CoordinateProcessor.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = self.smooth_angle(left_raw_angle, self.angle_buffer_left)
        
        right_raw_angle = CoordinateProcessor.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = self.smooth_angle(right_raw_angle, self.angle_buffer_right)
        
        # Use average of both arms for consistent tracking
        avg_angle = (left_angle + right_angle) / 2
        
        feedback = "Position detected"
        current_stage = self.stage
        
        # Overhead shoulder press logic
        if avg_angle > self.max_angle_threshold:
            if self.stage != "extended":
                self.stage = "extended"
                current_stage = "extended"
            feedback = "Arms fully extended overhead - excellent!"
            
        elif avg_angle < self.min_angle_threshold and self.stage == "extended":
            if self.stage != "bent":
                self.stage = "bent"
                current_stage = "bent"
                self.counter += 1
                feedback = f"Rep {self.counter} completed! Press back up"
            else:
                feedback = "Hold at shoulder level"
                
        elif self.min_angle_threshold <= avg_angle <= self.max_angle_threshold:
            if self.stage == "extended":
                feedback = "Lower dumbbells to shoulder level"
            elif self.stage == "bent":
                feedback = "Press dumbbells overhead"
            else:
                feedback = "Start with dumbbells at shoulder level"
        else:
            feedback = f"Current angle: {int(avg_angle)}°"
        
        return self.counter, feedback, int(avg_angle), current_stage or "ready"
