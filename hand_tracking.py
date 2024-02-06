import cv2
import time
from fingertip_tracking import FingertipTracker
from drawing_tool import DrawingTool
from eraser_tool import EraserTool

# Initialize FingertipTracker, DrawingTool, and EraserTool
fingertip_tracker = FingertipTracker()
drawing_tool = DrawingTool()
eraser_tool = EraserTool()
is_drawing_enabled = False
is_erasing = False  # Variable to track erasing status
fist_closed_counter = 0
fist_closed_threshold = 5
last_toggle_time = 0
toggle_delay = 2  # Delay in seconds between toggles

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)

    if not success:
        continue

    image = fingertip_tracker.track(image)

    # Determine which hand is which
    left_hand_index = None
    right_hand_index = None
    if fingertip_tracker.handedness:
        for i, hand_label in enumerate(fingertip_tracker.handedness):
            if hand_label == 'Left':
                left_hand_index = i
            elif hand_label == 'Right':
                right_hand_index = i

    current_time = time.time()
    if current_time - last_toggle_time > toggle_delay:
        # Toggle drawing on and off using the left hand fist gesture
        if left_hand_index is not None and fingertip_tracker.is_fist_closed(left_hand_index):
            fist_closed_counter += 1
            if fist_closed_counter > fist_closed_threshold:
                is_drawing_enabled = not is_drawing_enabled
                last_toggle_time = time.time()
                fist_closed_counter = 0
        else:
            fist_closed_counter = 0

    # Check for erasing gesture and drawing with the right hand
    if right_hand_index is not None:
        fingertip = fingertip_tracker.get_index_fingertip(image, right_hand_index)
        erasing = fingertip_tracker.is_erasing_gesture(right_hand_index)

        if erasing:
            is_erasing = True  # Set erasing status
            drawing_tool.drawing_points = eraser_tool.erase(drawing_tool.drawing_points, fingertip)
        elif fingertip and is_drawing_enabled and not erasing:
            is_erasing = False  # Reset erasing status
            drawing_tool.add_point(fingertip)

    # Display the drawing and erasing status
    status_text = "Drawing ON" if is_drawing_enabled else "Drawing OFF"
    cv2.putText(image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    if is_erasing:
        cv2.putText(image, "Erasing", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = drawing_tool.draw(image, drawing_tool.get_points())
    cv2.imshow('Hand Tracking with Drawing', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
