import cv2

class DrawingTool:
    def __init__(self):
        # Initialize a list to store points where the drawing will occur.
        self.drawing_points = []

    def draw(self, image, points):
        # Draw circles on the image at each point in the points list.
        for point in points:
            # Draw a green circle of radius 5 at each point.
            cv2.circle(image, point, 5, (0, 255, 0), cv2.FILLED)
        # Return the image with the drawings.
        return image

    def add_point(self, point):
        # Add a new point to the drawing_points list.
        self.drawing_points.append(point)

    def get_points(self):
        # Return the list of points where drawings have occurred.
        return self.drawing_points
