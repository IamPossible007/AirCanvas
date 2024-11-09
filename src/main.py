import cv2
import numpy as np
from hand_tracker import HandTracker
from canvas_manager import CanvasManager

def main():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    hand_tracker = HandTracker()
    canvas = CanvasManager(width, height)
    
    # UI Panel Configuration
    panel_height = 80
    button_size = 50
    spacing = 10
    start_x = 20
    start_y = 15  # Centered vertically in panel
    
    # Create color buttons
    color_buttons = {}
    x_position = start_x
    for color in canvas.colors.keys():
        color_buttons[color] = ((x_position, start_y), 
                              (x_position + button_size, start_y + button_size))
        x_position += button_size + spacing
    
    # Create eraser button
    eraser_x = x_position + spacing
    eraser_button = ((eraser_x, start_y), 
                    (eraser_x + button_size, start_y + button_size))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)  # Mirror image
        
        # Create UI panel as a numpy array
        panel = np.ones((panel_height, width, 3), dtype=np.uint8) * 240
        
        # Draw color buttons on panel
        for color, ((x1, y1), (x2, y2)) in color_buttons.items():
            # Draw button
            cv2.rectangle(panel, (x1, y1), (x2, y2), canvas.colors[color], -1)
            # Draw white outline for selected color
            if color == canvas.current_color and not canvas.is_eraser_mode:
                cv2.rectangle(panel, (x1-2, y1-2), (x2+2, y2+2), (255, 255, 255), 2)
            # Draw black outline for all buttons
            cv2.rectangle(panel, (x1, y1), (x2, y2), (0, 0, 0), 1)
        
        # Draw eraser button
        ((ex1, ey1), (ex2, ey2)) = eraser_button
        cv2.rectangle(panel, (ex1, ey1), (ex2, ey2), (200, 200, 200), -1)
        # Draw eraser icon
        cv2.putText(panel, "E", (ex1 + 15, ey2 - 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # Highlight if eraser is selected
        if canvas.is_eraser_mode:
            cv2.rectangle(panel, (ex1-2, ey1-2), (ex2+2, ey2+2), (255, 255, 255), 2)
        cv2.rectangle(panel, (ex1, ey1), (ex2, ey2), (0, 0, 0), 1)
        
        # Find hands
        hand_tracker.find_hands(frame)
        landmarks = hand_tracker.get_hand_position(frame)
        
        if landmarks:
            # Get finger positions
            index_finger = None
            middle_finger = None
            thumb = None
            
            for id, x, y in landmarks:
                if id == 4:  # Thumb tip
                    thumb = (x, y)
                elif id == 8:  # Index finger tip
                    index_finger = (x, y)
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                elif id == 12:  # Middle finger tip
                    middle_finger = (x, y)
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            
            if index_finger:
                ix, iy = index_finger
                
                # Check UI interactions
                if iy < panel_height:  # Only check button clicks in panel area
                    # Check color buttons
                    for color, ((x1, y1), (x2, y2)) in color_buttons.items():
                        if x1 < ix < x2 and y1 < iy < y2:
                            canvas.change_color(color)
                            break
                    
                    # Check eraser button
                    if ex1 < ix < ex2 and ey1 < iy < ey2:
                        canvas.set_eraser_mode()
                else:
                    # Drawing mode
                    canvas.draw(index_finger)
            
            # Clear canvas with thumb and index pinch
            if thumb and index_finger:
                if np.sqrt(((thumb[0] - index_finger[0]) ** 2 + 
                          (thumb[1] - index_finger[1]) ** 2)) < 40:
                    canvas.clear()
        else:
            canvas.prev_point = None
        
        # Combine panel, canvas and camera frame
        canvas_frame = canvas.get_canvas()
        combined = cv2.addWeighted(frame, 0.7, canvas_frame, 0.3, 0)
        combined[0:panel_height, 0:width] = panel
        
        # Show current tool
        tool_text = "ERASER" if canvas.is_eraser_mode else f"COLOR: {canvas.current_color.upper()}"
        cv2.putText(combined, tool_text, (width - 200, panel_height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        cv2.imshow("Air Canvas", combined)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas.clear()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()