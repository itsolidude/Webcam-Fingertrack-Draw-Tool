import cv2
from fingertip_tracking import FingertipTracker
from drawing_tool import DrawingTool

# Initialize FingertipTracker and DrawingTool and other things
fingertip_tracker = FingertipTracker()
drawing_tool = DrawingTool()
is_drawing_enabled = False


# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)

    if not success:
        continue

    # Track fingertip
    image = fingertip_tracker.track(image)
    fingertip = fingertip_tracker.get_index_fingertip(image)
    
    # Check if the fist is closed to toggle drawing
    if fingertip_tracker.is_fist_closed():
        is_drawing_enabled = not is_drawing_enabled

    if fingertip:
        drawing_tool.add_point(fingertip)

    # Draw points
    image = drawing_tool.draw(image, drawing_tool.get_points())

    # Display the image.
    cv2.imshow('Hand Tracking with Drawing', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close the OpenCV window.
cap.release()
cv2.destroyAllWindows()
