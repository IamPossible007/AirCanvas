import cv2
import numpy as np

class CanvasManager:
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.canvas.fill(255)  # White background
        self.drawing_color = (0, 0, 255)  # Default red color
        self.drawing_thickness = 5
        self.eraser_thickness = 40
        self.prev_point = None
        self.colors = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'purple': (255, 0, 255),
            'black': (0, 0, 0)
        }
        self.current_color = 'red'
        self.is_eraser_mode = False
        
    def draw(self, point):
        if self.prev_point is not None:
            color = (255, 255, 255) if self.is_eraser_mode else self.drawing_color
            thickness = self.eraser_thickness if self.is_eraser_mode else self.drawing_thickness
            cv2.line(self.canvas, self.prev_point, point, color, thickness)
        self.prev_point = point
        
    def clear(self):
        self.canvas.fill(255)
        self.prev_point = None
        
    def change_color(self, color_name):
        if color_name in self.colors:
            self.current_color = color_name
            self.drawing_color = self.colors[color_name]
            self.is_eraser_mode = False
            
    def set_eraser_mode(self):
        self.is_eraser_mode = True
        
    def get_canvas(self):
        return self.canvas.copy()