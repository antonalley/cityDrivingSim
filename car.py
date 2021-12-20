import numpy as np

from CONSTANTS import *
import pygame
import numpy
from AI_v0_2 import Network as BACKGROUND_AI

NETWORK_SHAPE = [7, 5, 3] # TODO Train this size untill it's the best it can do, then add a layer at a time.

class Car(BACKGROUND_AI):
    def __init__(self, position: tuple, direction=S, file=None):
        BACKGROUND_AI.__init__(self, networkShape=NETWORK_SHAPE, file=file)
        self.nextMove = {} # {"direction", "pos", "velocity"}
        self.velocity = direction[0]*3, direction[1]*3 # (0, 1)  # x, y change per frame
        self.pos = position  # The center of the car
        self.width = CARWIDTH
        self.height = CARLENGTH
        self.direction = direction  # The direction it is facing
        self.topLeft = (0, 0)
        self.align_topLeft()
        self.color = BLUE

        # For the learning Model:
        self.RelativeSensors = [[] for i in range(6)]
        self.initialize_sensors()

    def next_move(self): #, result = [0, 0, 0]):
        """Takes the current state of game and determines what the next move will be, without making any changes yet"""
        result = [0, 0, 0]  # Turn, LaneChange, Acceleration TODO Temporary- do the calculations here
        result = self.feedForward([1,0,0,0,0,0,0]) # TODO get input vector from data from Map
        #print(result)
        if result[0]:  # Turn:
            if self.direction == N or self.direction == S:
                # Turn right is swap * -1; turn left is swap
                self.nextMove["direction"] = (-1 * result[0] * self.direction[1], -1 * result[0] * self.direction[0])
                self.nextMove["velocity"] = (-1 * result[0] * self.velocity[1], -1 * result[0] * self.velocity[0])
            else:
                # Turn right is swap, turn left is swap * -1
                self.nextMove["direction"] = (result[0] * self.direction[1], result[0] * self.direction[0])
                self.nextMove["velocity"] = (result[0] * self.velocity[1], result[0] * self.velocity[0])
            self.nextMove["pos"] = self.pos  # Doesn't change, but needs to be initialized.

        if result[1]:  # Lane Change:
            if self.direction == N or self.direction == S:
                self.pos = self.pos[0] + (LANEWIDTH * result[1] * -self.direction[1]), self.pos[1]
            else:
                self.pos = self.pos[0], self.pos[1] + (LANEWIDTH * result[1] * self.direction[0])

        if result[2]:  # Acceleration
            self.velocity = (self.velocity[0] + (result[2] * self.direction[0]), self.velocity[1] + (result[2] * self.direction[1]))

        return self.nextMove["pos"]  # So it can check for collisions on the map

    def update(self, isCollision: bool):
        """puts the next move into action"""
        if not isCollision and self.nextMove:
            self.direction = self.nextMove["direction"]
            self.pos = self.nextMove["pos"]
            self.velocity = self.nextMove["velocity"]


        # Advance by the velocity
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        self.align_topLeft()

        self.nextMove = {}
        return None

    def align_topLeft(self):
        """align the topleft corner with the pos for pygame drawing"""
        if self.direction == N or self.direction == S:
            self.topLeft = (self.pos[0] - self.height // 2, self.pos[1] - self.width // 2)
        else:
            self.topLeft = (self.pos[0] - self.width // 2, self.pos[1] - self.height // 2)

    def initialize_sensors(self):
        """returns list of every sensor with every relative to self.pos x,y coordinate in it"""
        # Forward: len = 38
        self.RelativeSensors[0] = [(0,y) for y in range(self.height//2, self.height*2 + self.height//2)]
        # LeftForward: len = 19
        self.RelativeSensors[1] = [(-y - self.width // 2, y) for y in range(self.height)]
        # RightForward: len = 19
        self.RelativeSensors[2] = [(y + self.width // 2, y) for y in range(self.height)]
        # Left back: len = 19
        self.RelativeSensors[3] = [(-y - self.width // 2, -y) for y in range(self.height)]
        # Right back: len = 19
        self.RelativeSensors[4] = [(y + self.width // 2, -y) for y in range(self.height)]
        # Backward: len = 19
        self.RelativeSensors[5] = [(0, -y) for y in range(self.height // 2, self.height + (self.height // 2))]

    def generate_sensors(self):
        ''' Calculates the actual sensor position based on the current position and the relative sensors'''
        pass


    def collision_check(self, otherCar):
        pass


    def display(self, surface):
        """surface is a pygame.Surface object to blit the car onto"""
        if self.direction == N or self.direction == S:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.topLeft, (self.width, self.height)))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.topLeft, (self.height, self.width)))
        return surface