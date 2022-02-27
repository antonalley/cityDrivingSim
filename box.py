class Box:
    """
    A Base class that can be implemented by intersection, car, possibly road
    """
    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height

    def line_intercept(self, line_start, line_end):
        """
        @:param line_start where the line starts
        @:param line_end where the line ends
        @:return a boolean to say if the line intercepts the box
        """

    def get_lines(self):
        """
        :return: 4 lines that make up the box
        """
        lines = []
        lines.append((self.topLeft, (self.topLeft[0]+self.width, self.topLeft[1])))  # Top Line
        lines.append((self.topLeft, (self.topLeft[0], self.topLeft[1] + self.height)))  # Left Line
        lines.append(((self.topLeft[0], self.topLeft[1] + self.height), (self.topLeft[0] + self.width, self.topLeft[1] + self.height)))  # Bottom Line
        lines.append(((self.topLeft[0]+self.width, self.topLeft[1]), (self.topLeft[0] + self.width, self.topLeft[1] + self.height)))  # Right

        return lines