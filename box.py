class Box:
    """
    A Base class that can be implemented by intersection, car, possibly road
    To give it the basic properties of a box that need to be assessed
    """
    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height

    def calcLine(self, x = 0, line_start = [0,0], line_end = [1,0]): #parameters are for the sensor line

        slope = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0]) #calculates the slope of the sensor line

        return slope * (x - line_end[0]) + line_end[1] #returns point-slope form of the sensor

    def line_intercept(self, line_start, line_end):
        """
        @:param line_start where the line starts
        @:param line_end where the line ends
        @:return coordinate of where it intercepts, or False if it doesn't intercept

        """
        lineWidth = line_end[0] - line_start[0]
        lineHeight = line_end[1] - line_start[1]

        xLines = [self.get_lines()[0], self.get_lines()[1]]
        yLines = [self.get_lines()[2],self.get_lines()[3]]


        point = []
        if lineHeight == 0:
           for x in range(lineWidth + 1):
               if self.calcLine(x) in xLines:
                   inter = True
                   point.append([x,self.calcLine(x)])
        elif lineWidth == 0:
            for y in range(lineHeight + 1):
                if self.calcLine(y) in yLines:
                    inter = True
                    point.append(self.calcLine(y), y)
        else:
            inter = False

        if len(point) == 0:
            return inter
        else:
            return point

    def get_lines(self):
        """
        :return: 4 lines that make up the box
        """
        lines = []

        lines.append(self.topLeft[0]) #first vertical line
        lines.append(self.topLeft[0] + self.width) #far right vertical line
        lines.append(self.topLeft[1]) #top horizontal line
        lines.append(self.topLeft[1] + self.height) #bottom horizontal line

        return lines