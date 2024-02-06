import cv2
import mediapipe as mp

class FingertipTracker:
    def __init__(self):
        """
        Initialize the FingertipTracker with MediaPipe Hands solution.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.handedness = []  # To store the handedness (left or right) of each hand detected.

    def track(self, image):
        """
        Process the image to find hand landmarks.
        :param image: The image frame from the webcam.
        :return: The processed image.
        """
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        # Reset handedness information for each frame
        self.handedness = []

        # Store handedness information
        if self.results.multi_handedness:
            for hand_handedness in self.results.multi_handedness:
                self.handedness.append(hand_handedness.classification[0].label)

        return image

    def get_index_fingertip(self, image, hand_no=0):
        """
        Get the position of the index fingertip.
        :param image: The image frame from the webcam.
        :param hand_no: The index of the hand (0 for the first hand, 1 for the second, etc.).
        :return: The (x, y) coordinates of the index fingertip or None if not found.
        """
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            index_fingertip = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, c = image.shape
            x, y = int(index_fingertip.x * w), int(index_fingertip.y * h)
            return x, y
        return None

    def is_fist_closed(self, hand_no=0):
        """
        Check if the fist of a specified hand is closed.
        :param hand_no: The index of the hand.
        :return: True if the fist is closed, False otherwise.
        """
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            landmarks = hand.landmark
            fingertips = [
                self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                self.mp_hands.HandLandmark.RING_FINGER_TIP,
                self.mp_hands.HandLandmark.PINKY_TIP
            ]
            wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
            for fingertip_id in fingertips:
                fingertip = landmarks[fingertip_id]
                if fingertip.y < wrist.y:
                    return False
            return True
        return False

    def is_erasing_gesture(self, hand_no=0):
        """
        Check if the erasing gesture is made with a specified hand.
        :param hand_no: The index of the hand.
        :return: True if the erasing gesture is detected, False otherwise.
        """
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            landmarks = hand.landmark
            thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            def are_points_close(point1, point2, threshold=0.05):
                return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) < threshold ** 2
            if are_points_close(thumb_tip, index_tip) and are_points_close(index_tip, middle_tip):
                return True
        return False
