import cv2

class DrawingTool:
    def __init__(self):
        # Initialize a list to store points where the drawing will occur.
        self.drawing_points = []

    def draw(self, image, points):
        for i in range(1, len(points)):
            cv2.line(image, points[i - 1], points[i], (0, 255, 0), thickness=2)
        return image

    def add_point(self, point):
        # Add a new point to the drawing_points list.
        self.drawing_points.append(point)

    def get_points(self):
        # Return the list of points where drawings have occurred.
        return self.drawing_points
