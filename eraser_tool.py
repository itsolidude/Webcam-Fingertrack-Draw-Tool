class EraserTool:
    def __init__(self, eraser_size=20):
        """
        Initialize the eraser tool with a specified size.
        :param eraser_size: The radius of the eraser.
        """
        self.eraser_size = eraser_size

    def erase(self, drawing_points, erase_point):
        """
        Erase points from the drawing.
        :param drawing_points: List of points in the drawing.
        :param erase_point: The current point of the eraser.
        :return: Updated list of points after erasing.
        """
        new_drawing_points = [point for point in drawing_points if not self.is_point_near(point, erase_point)]
        return new_drawing_points

    def is_point_near(self, point, erase_point):
        """
        Check if a point is within the eraser radius of the erase_point.
        :param point: A point from the drawing.
        :param erase_point: The current point of the eraser.
        :return: True if the point is within the eraser radius, False otherwise.
        """
        return (point[0] - erase_point[0]) ** 2 + (point[1] - erase_point[1]) ** 2 < self.eraser_size ** 2
