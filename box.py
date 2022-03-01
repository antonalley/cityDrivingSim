import numpy as np

class Box:
    """
    A Base class that can be implemented by intersection, car, possibly road
    To give it the basic properties of a box that need to be assessed
    """

    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height

    def line_intercept(self, line_start, line_end):
        """
        @:param line_start where the line starts
        @:param line_end where the line ends
        @:return coordinate of where it intercepts, or False if it doesn't intercept
        """
        my_lines = self.get_lines()
        my_points = self.get_points_in_line(*my_lines[0]) + self.get_points_in_line(*my_lines[1]) + \
                    self.get_points_in_line(*my_lines[2]) + self.get_points_in_line(*my_lines[3])
        their_points = self.get_points_in_line(line_start, line_end)

        for i in my_points:
            for j in their_points:
                if i == j:
                    return i

        return False

    def get_lines(self):
        """
        :return: 4 lines that make up the box
        """
        lines = []
        lines.append((self.topLeft, (self.topLeft[0] + self.width, self.topLeft[1])))  # Top Line
        lines.append((self.topLeft, (self.topLeft[0], self.topLeft[1] + self.height)))  # Left Line
        lines.append(((self.topLeft[0], self.topLeft[1] + self.height),
                      (self.topLeft[0] + self.width, self.topLeft[1] + self.height)))  # Bottom Line
        lines.append(((self.topLeft[0] + self.width, self.topLeft[1]),
                      (self.topLeft[0] + self.width, self.topLeft[1] + self.height)))  # Right

        return lines

    def get_points_in_line(self, start, end) -> list:
        x1, y1 = start
        x2, y2 = end

        points = []
        x_travels = (x2 - x1) / self.distance(start, end)
        y_travels = (y2 - y1) / self.distance(start, end)

        x_crawl = x1
        y_crawl = y1
        points.append((x_crawl, y_crawl))
        for i in range(round(self.distance(start, end))):
            # print(round(x_crawl), round(y_crawl))
            x_crawl += x_travels
            y_crawl += y_travels
            points.append((round(x_crawl), round(y_crawl)))
        # print(round(x_crawl), round(y_crawl))

        return points

    @staticmethod
    def distance(p1, p2):
        """
        :param p1: first point
        :param p2: second point
        :return: the distance between these 2 points
        """
        x1, y1 = p1
        x2, y2 = p2
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# For Testing:
if __name__ == "__main__":
    myBox = Box((10,10), 10, 10)
    print(myBox.line_intercept((20,20),(45,25)))