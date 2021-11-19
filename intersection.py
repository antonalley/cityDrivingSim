from CONSTANTS import *
import pygame
from road import Road
import random

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

    def swap_signal_state(self):
        for i, l in enumerate(self.signalState):
            if l == GREEN:
                self.signalState[i] = RED
            else:
                self.signalState[i] = GREEN

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