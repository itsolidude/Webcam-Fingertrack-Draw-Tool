import cv2
import mediapipe as mp

# Initialize MediaPipe Hand module.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing module.
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Flip the image horizontally for a later selfie-view display.
    # Convert the color space from BGR to RGB.
    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands.
    results = hands.process(image)

    # Draw hand landmarks.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the image.
    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close the OpenCV window.
cap.release()
cv2.destroyAllWindows()
