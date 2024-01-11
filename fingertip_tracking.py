import cv2
import mediapipe as mp

class FingertipTracker:
    def __init__(self):
        # Initialize the MediaPipe hands solution.
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        # Initialize MediaPipe drawing utilities for visualizing hand landmarks.
        self.mp_drawing = mp.solutions.drawing_utils

    def track(self, image):
        # Convert the image from BGR (OpenCV format) to RGB (MediaPipe format).
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the RGB image to find hand landmarks.
        self.results = self.hands.process(imageRGB)
        # Return the original image.
        return image

    def get_index_fingertip(self, image, hand_no=0):
        # Check if any hand landmarks were detected.
        if self.results.multi_hand_landmarks:
            # Select the specified hand based on hand_no.
            hand = self.results.multi_hand_landmarks[hand_no]
            # Get the landmark for the index fingertip.
            index_fingertip = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # Calculate the height, width, and channels of the image.
            h, w, c = image.shape
            # Convert the relative position of the fingertip to pixel coordinates.
            x, y = int(index_fingertip.x * w), int(index_fingertip.y * h)
            # Return the pixel coordinates of the index fingertip.
            return x, y
        # Return None if no hand landmarks are detected.
        return None
    
    def is_fist_closed(self, hand_no=0):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            landmarks = hand.landmark

            # Example check: Compare the tip of the index finger with a lower landmark
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            palm_base = landmarks[self.mp_hands.HandLandmark.WRIST]

            # Check if the index finger is close to the base of the palm
            if index_tip.y > palm_base.y:  # y-coordinate is higher for lower screen positions
                return True
        return False
    
