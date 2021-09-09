# simulateLogic.py
import random

import pygame
from CONSTANTS import *


class CityMap:
    def __init__(self, layout: "default or custom?" = "default"):
        self.cars = []
        self.roads = []
        self.intersections = []

        if layout == "default":  # Will show chicago style roads
            self.roads.append(Road((0, HEIGHT - LANEWIDTH * 5), (WIDTH, HEIGHT - LANEWIDTH * 5), 8, E))  # Bottom Big Road 8 lanes
            self.roads.append(Road((LANEWIDTH * 4, 0), (LANEWIDTH * 4, HEIGHT), 6, S))  # Left big 6 lane road
            self.roads.append(Road((WIDTH - LANEWIDTH * 5, 0), (WIDTH - LANEWIDTH * 5, HEIGHT), 8, S))  # Right big road 8 lanes
            self.roads.append(Road((0, LANEWIDTH * 3), (WIDTH, LANEWIDTH * 3), 4, E))  # Top Road 4 lanes
            self.roads.append(Road((WIDTH // 2, LANEWIDTH * 3), (WIDTH // 2, HEIGHT - LANEWIDTH), 4, S))  # Middle 4 lane road
            for qq in range(3): # Small E-W streets
                self.roads.append(Road((LANEWIDTH * 3, LANEWIDTH * 10 + qq * WIDTH // 10),
                                       (WIDTH - LANEWIDTH, LANEWIDTH * 10 + qq * WIDTH // 10), 2, E))

            self.roads.append(Road((WIDTH // 4, LANEWIDTH * 10),
                                   (WIDTH // 4, LANEWIDTH * 11 + 2 * WIDTH // 10), 2, S))

            for e, r in enumerate(self.roads):  # This does
                for r2 in self.roads[e:]:
                    signal_type = "stops" if r.num_lanes + r2.num_lanes <= 6 else "lights"
                    try:
                        if r.direction == N or r.direction == S:
                            I = Intersection(r, r2, signal_type)
                        else:
                            I = Intersection(r2, r, signal_type)
                    except ValueError:  # the roads don't intersect
                        pass
                    else:
                        self.intersections.append(I)

            self.initialize_cars()

    def initialize_cars(self):
        for road in self.roads:
            if road.direction == N or road.direction == S:
                self.cars.append(Car((road.start[0] - LANEWIDTH // 2, road.start[1])))
            else:
                self.cars.append(Car((road.start[0], road.start[1] - LANEWIDTH // 2)))

    def check_pixel(self, x, y):
        """Finds at Position(x,y) what is there on the map"""
        return 0  # Value 0-6 sensorValue

    def display(self, surface):
        for road in self.roads:
            road.display(surface)
        for i in self.intersections:
            i.display(surface)
        for car in self.cars:
            car.display(surface)

        return 0




class Road:
    def __init__(self, start, end, num_lanes, direction):
        """the start and end are tuples that are in the center of the road"""
        self.num_lanes = num_lanes
        self.start = start
        self.width = num_lanes * LANEWIDTH
        self.end = end
        self.lines = []  # {type:, start:, end:}
        self.direction = direction
        #self.road_rect = pygame.Rect(0,0,0,0)
        if direction == N or direction == S:
            self.lines.append({"type": "SOLID", "start": (self.start[0] - self.width//2, self.start[1]),
                               "end": (self.end[0] - self.width//2, self.end[1])})  # Outer left
            self.lines.append({"type": "SOLID", "start": (self.start[0] + self.width//2, self.start[1]),
                               "end": (self.end[0] + self.width//2, self.end[1])})  # Outer Right
            self.lines.append({"type": "SOLID", "start": self.start,
                               "end": self.end})  # Center

            if num_lanes > 2:
                for i in range(1, (num_lanes-2) // 2 + 1):  # there is an i value for each lane to add on both sides. Can only have even number
                    self.lines.append({"type": "DOTTED", "start": (self.start[0] - (i * LANEWIDTH), self.start[1]), "end": (self.end[0] - (i * LANEWIDTH), self.end[1])})
                    self.lines.append({"type": "DOTTED", "start": (self.start[0] + (i * LANEWIDTH), self.start[1]), "end": (self.end[0] + (i * LANEWIDTH), self.end[1])})

        else:  # If e or w
            self.lines.append({"type": "SOLID", "start": (self.start[0], self.start[1] - self.width // 2),
                               "end": (self.end[0], self.end[1] - self.width // 2)})  # Outer left
            self.lines.append({"type": "SOLID", "start": (self.start[0], self.start[1] + self.width // 2),
                               "end": (self.end[0], self.end[1] + self.width // 2)})  # Outer Right
            self.lines.append({"type": "SOLID", "start": self.start,
                               "end": self.end})  # Center
            if num_lanes > 2:
                for i in range(1, (num_lanes-2) // 2 + 1):  # there is an i value for each lane to add on both sides. Can only have even number
                    self.lines.append({"type": "DOTTED", "start": (self.start[0], self.start[1] - (i * LANEWIDTH)), "end": (self.end[0], self.end[1] - (i * LANEWIDTH))})
                    self.lines.append({"type": "DOTTED", "start": (self.start[0], self.start[1] + (i * LANEWIDTH)), "end": (self.end[0], self.end[1] + (i * LANEWIDTH))})
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
                    c = round(math.sqrt(a ** 2 + b ** 2))
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


class Intersection:
    def __init__(self, road1: Road, road2: Road, signal_type: "lights or stops or none" = "none"):
        """road1 and road2 are Road object, point_of_crossing is the topleft point the 2 roads meet
        road 1 will be the one that enters and exits on the north and south, road2 on the east and west
        """
        self.center = road1.find_crossing(road2)
        self.width = road1.width
        self.height = road2.width
        self.topLeft = (self.center[0] - self.width // 2, self.center[1] - self.height // 2)
        self.signalType = signal_type
        if self.signalType == "lights":
            if random.uniform(0, 1) >= 0.5:
                self.signalState = [GREEN, RED, GREEN, RED]  # In order of cars in lanes moving south, west, north, east
            else:
                self.signalState = [RED, GREEN, RED, GREEN]  # In order of cars in lanes moving south, west, north, east
        if self.center == (300, 120):
            print("Broken intersection: (width, height):", self.width, self.height)
            print("topleft: ", self.topLeft)

    def display(self, surface):
        """surface is a pygame.Surface object to blit the Intersection onto"""
        pygame.draw.rect(surface, BLACK, pygame.Rect(self.topLeft, (self.width, self.height)))
        # draw traffic signals, stop signs
        if self.signalType == "lights":
            pygame.draw.line(surface, self.signalState[0],
                             (self.topLeft[0], self.topLeft[1] + self.height),
                             (self.center[0], self.topLeft[1] + self.height),
                             LINEWIDTH * 3)  # South bound
            pygame.draw.line(surface, self.signalState[1],
                             self.topLeft,
                             (self.topLeft[0], self.center[1]),
                             LINEWIDTH * 3)  # West bound
            pygame.draw.line(surface, self.signalState[2],
                             (self.center[0], self.topLeft[1]),
                             (self.topLeft[0] + self.width, self.topLeft[1]),
                             LINEWIDTH * 3)  # North bound
            pygame.draw.line(surface, self.signalState[3],
                             (self.topLeft[0] + self.width, self.center[1]),
                             (self.topLeft[0] + self.width, self.topLeft[1] + self.height),
                             LINEWIDTH * 3)  # East bound
        elif self.signalType == "stops":
            pygame.draw.rect(surface, RED, pygame.Rect((self.topLeft[0] - LANEWIDTH, self.topLeft[1] - LANEWIDTH),
                                                       (LANEWIDTH, LANEWIDTH)))
            pygame.draw.rect(surface, RED, pygame.Rect((self.topLeft[0] + self.width, self.topLeft[1] + self.height),
                                                       (LANEWIDTH, LANEWIDTH)))
            pygame.draw.rect(surface, RED, pygame.Rect((self.topLeft[0] + self.width, self.topLeft[1] - LANEWIDTH),
                                                       (LANEWIDTH, LANEWIDTH)))
            pygame.draw.rect(surface, RED, pygame.Rect((self.topLeft[0] - LANEWIDTH, self.topLeft[1] + self.height),
                                                       (LANEWIDTH, LANEWIDTH)))
        return surface


class Car:
    def __init__(self, position: tuple):
        self.nextMove = []
        self.velocity = (0, 0)  # x, y change per frame
        self.angular_velocity = (0, 0)  # x, y change of velocity per frame
        self.pos = position  # The center of the car
        self.width = round(LANEWIDTH * 0.75)
        self.height = round(LANEWIDTH * 1.25)
        self.direction = N # TODO implement the direction into the final RECT and figure out how to get it on an angle
        self.topLeft = (self.pos[0] - self.width //2, self.pos[1] - self.height // 2)
        self.color = BLUE

    def next_move(self):
        """Takes the current state of game and determines what the next move will be, without making any changes yet"""
        result = 0  # TODO Temporary- do the calculations here
        self.nextMove = result
        return 0;

    def update(self):
        """puts the next move into action"""
        return None

    def generate_sensors(self):
        """returns list of every sensor with every x,y coordinate in it"""
        return []

    def display(self, surface):
        """surface is a pygame.Surface object to blit the car onto"""
        pygame.draw.rect(surface, self.color, pygame.Rect(self.topLeft, (self.width, self.height)))
        return surface

'''
# JUST FOR TESTING:
xs = []

for i in range(10):
    xs.append(Road((i*150 + 50, 0), (i*150 + 50, 800), 2, S))
    xs.append(Road((0,i*100 + 50), (1200, i*100 + 50), 4, E))
    xs.append(Intersection(xs[-2], xs[-1]))

myCar = Car()
myCar.topLeft = (50-LANEWIDTH + round(0.125*LANEWIDTH), 10)
xs.append(myCar)

hi = pygame.Surface((1200, 800))
hi.fill(GRAY)

DISPLAY = pygame.display.set_mode((1200, 800), 0, 32)
pygame.init()

import sys
from pygame.locals import QUIT
import random

while True:
    DISPLAY.fill(GRAY)
    for x in xs:
        x.display(hi)
    DISPLAY.blit(hi, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
'''