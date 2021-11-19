from CONSTANTS import *
import pygame
import numpy

class Road:
    def __init__(self, start, end, num_lanes, direction):
        """the start and end are tuples that are in the center of the road"""
        self.num_lanes = num_lanes
        self.start = start
        self.width = num_lanes * LANEWIDTH
        self.end = end
        self.lines = []  # {type:, start:, end:}
        self.direction = direction
        # self.road_rect = pygame.Rect(0,0,0,0)
        if direction == N or direction == S:
            self.lines.append({"type": "SOLID", "start": (self.start[0] - self.width // 2, self.start[1]),
                               "end": (self.end[0] - self.width // 2, self.end[1])})  # Outer left
            self.lines.append({"type": "SOLID", "start": (self.start[0] + self.width // 2, self.start[1]),
                               "end": (self.end[0] + self.width // 2, self.end[1])})  # Outer Right
            self.lines.append({"type": "SOLID", "start": self.start,
                               "end": self.end})  # Center

            if num_lanes > 2:
                for i in range(1, (
                                          num_lanes - 2) // 2 + 1):  # there is an i value for each lane to add on both sides. Can only have even number
                    self.lines.append({"type": "DOTTED", "start": (self.start[0] - (i * LANEWIDTH), self.start[1]),
                                       "end": (self.end[0] - (i * LANEWIDTH), self.end[1])})
                    self.lines.append({"type": "DOTTED", "start": (self.start[0] + (i * LANEWIDTH), self.start[1]),
                                       "end": (self.end[0] + (i * LANEWIDTH), self.end[1])})

        else:  # If e or w
            self.lines.append({"type": "SOLID", "start": (self.start[0], self.start[1] - self.width // 2),
                               "end": (self.end[0], self.end[1] - self.width // 2)})  # Outer left
            self.lines.append({"type": "SOLID", "start": (self.start[0], self.start[1] + self.width // 2),
                               "end": (self.end[0], self.end[1] + self.width // 2)})  # Outer Right
            self.lines.append({"type": "SOLID", "start": self.start,
                               "end": self.end})  # Center
            if num_lanes > 2:
                for i in range(1, (
                                          num_lanes - 2) // 2 + 1):  # there is an i value for each lane to add on both sides. Can only have even number
                    self.lines.append({"type": "DOTTED", "start": (self.start[0], self.start[1] - (i * LANEWIDTH)),
                                       "end": (self.end[0], self.end[1] - (i * LANEWIDTH))})
                    self.lines.append({"type": "DOTTED", "start": (self.start[0], self.start[1] + (i * LANEWIDTH)),
                                       "end": (self.end[0], self.end[1] + (i * LANEWIDTH))})
        # Extra lanes:
        self.width += 6  # Gives a shoulder to the Roads

    @staticmethod
    def ccw(A, B, C):  # Used from https://stackoverflow.com/a/9997374/6876267
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def find_crossing(self, other_road):
        A, B = self.start, self.end
        C, D = other_road.start, other_road.end
        isCrossing = Road.ccw(A, C, D) != Road.ccw(B, C, D) and Road.ccw(A, B, C) != Road.ccw(A, B, D)
        if not isCrossing:
            raise ValueError("These two roads do not intersect!!", self, other_road)
        return max(self.start[0], other_road.start[0]), max(self.start[1], other_road.start[1])

    def display(self, surface):
        """surface is a pygame.Surface object to blit the road onto"""
        self.road_rect = pygame.draw.line(surface, BLACK, self.start, self.end, self.width)
        # Draw lines on top of road:
        for line in self.lines:
            if line["type"] == "SOLID":
                pygame.draw.line(surface, WHITE, line["start"], line["end"], LINEWIDTH)
            else:  # Draw Dotted line
                # taken from https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame
                x1, y1 = line["start"]
                x2, y2 = line["end"]
                dl = DOTTEDLINELENGTH

                if x1 == x2:
                    ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
                    xcoords = [x1] * len(ycoords)
                elif y1 == y2:
                    xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
                    ycoords = [y1] * len(xcoords)
                else:
                    a = abs(x2 - x1)
                    b = abs(y2 - y1)
                    c = round(numpy.sqrt(a ** 2 + b ** 2))
                    dx = dl * a / c
                    dy = dl * b / c

                    xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
                    ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

                next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
                last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
                for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
                    start = (round(x1), round(y1))
                    end = (round(x2), round(y2))
                    pygame.draw.line(surface, WHITE, start, end, LINEWIDTH)

        return surface