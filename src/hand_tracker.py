import mediapipe as mp
import cv2
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.drawing = False
        self.points = []
        
    def find_hands(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        return self.results
    
    def get_hand_position(self, frame):
        height, width, _ = frame.shape
        landmarks = []
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                # Draw hand landmarks for visualization
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    landmarks.append((id, cx, cy))
                
                if len(landmarks) >= 12:
                    index_tip = landmarks[8]   
                    middle_tip = landmarks[12]
                    distance = np.sqrt((middle_tip[1] - index_tip[1])**2 + 
                                     (middle_tip[2] - index_tip[2])**2)
                    
                    self.drawing = distance > 30  
                    
                    # If drawing, add index finger tip position to points
                    if self.drawing and index_tip:
                        self.points.append((index_tip[1], index_tip[2]))
                    
        return landmarks
    
    def draw_on_frame(self, frame):
        if len(self.points) > 1:
            for i in range(1, len(self.points)):
                if self.points[i-1] is not None and self.points[i] is not None:
                    cv2.line(frame, self.points[i-1], self.points[i], (0, 255, 0), 2)
        return frame