import numpy as np

from CONSTANTS import *
import pygame
from AI_v0_2 import Network as BACKGROUND_AI

NETWORK_SHAPE = [42, 14, 7, 3]  # TODO Train this size until it's the best it can do, then add a layer at a time.


class Car(BACKGROUND_AI):
    def __init__(self, position: tuple, direction=S, file=None):
        BACKGROUND_AI.__init__(self, networkShape=NETWORK_SHAPE, file=file)
        self.nextMove = {}  # {"direction", "pos", "velocity"}
        self.velocity = np.array([direction[0] * 3, direction[1] * 3])  # (0, 1)  # x, y change per frame
        self.pos = np.array(position)  # The center of the car
        self.width = CARWIDTH
        self.height = CARLENGTH
        self.direction = direction  # The direction it is facing
        self.topLeft = (0, 0)
        self.align_topLeft()
        self.color = BLUE

        # For the learning Model:
        self.sensors = []
        self.initialize_sensors()

    def next_move(self, city_map, keys_in=None):  # , result = [0, 0, 0]):
        """Takes the current state of game and determines what the next move will be, without making any changes yet"""
        if keys_in is None:
            keys_in = {}

        # result = [Turn, LaneChange, Acceleration]
        #result = self.feedForward([1, 0, 0, 0, 0, 0, 0])  # TODO get input vector from data from Map
        result = self.feedForward(self.get_sensor_data(city_map))
        # print(result)

        # These are to make sure that there aren't any errors with not having a value
        self.nextMove["direction"] = self.direction
        self.nextMove["pos"] = self.pos
        self.nextMove["velocity"] = self.velocity
        if result[0]:  # Turn:
            if (self.direction == N).all() or (self.direction == S).all():
                # Turn right is swap * -1; turn left is swap
                self.nextMove["direction"] = (normalizeResult(-1 * result[0] * self.direction[1]),
                                              normalizeResult(-1 * result[0] * self.direction[0]))
                self.nextMove["velocity"] = (-1 * result[0] * self.velocity[1], -1 * result[0] * self.velocity[0])
            else:
                # Turn right is swap, turn left is swap * -1
                self.nextMove["direction"] = (
                    normalizeResult(result[0] * self.direction[1]), normalizeResult(result[0] * self.direction[0]))
                self.nextMove["velocity"] = (result[0] * self.velocity[1], result[0] * self.velocity[0])
            self.nextMove["pos"] = self.pos  # Doesn't change, but needs to be initialized.

        if result[1]:  # Lane Change:
            if (self.direction == N).all() or (self.direction == S).all():
                self.nextMove["pos"] = self.pos[0] + (LANEWIDTH * result[1] * -self.direction[1]), self.pos[1]
            else:
                self.nextMove["pos"] = self.pos[0], self.pos[1] + (LANEWIDTH * result[1] * self.direction[0])

        if result[2]:  # Acceleration
            self.velocity = (
                self.velocity[0] + (result[2] * self.direction[0]), self.velocity[1] + (result[2] * self.direction[1]))

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
        if (self.direction == N).all() or (self.direction == S).all():
            self.topLeft = (self.pos[0] - self.width // 2, self.pos[1] - self.height // 2)
        else:
            self.topLeft = (self.pos[0] - self.height // 2, self.pos[1] - self.width // 2)

    def initialize_sensors(self):
        """returns list of every sensor with every relative to self.pos x,y coordinate in it"""
        # Forward: len = 38
        self.sensors.append(Sensor((0, -self.height // 2), (0, round(-self.height * 2.5))))
        # LeftForward: len = 19
        self.sensors.append(Sensor((-self.width // 2, 0), (- self.height - self.width // 2, -self.height)))
        # RightForward: len = 19
        self.sensors.append(Sensor((self.width // 2, 0), (self.height + self.width // 2, -self.height)))
        # Left back: len = 19
        self.sensors.append(Sensor((-self.width // 2, 0), (-self.height - self.width // 2, self.height)))
        # Right back: len = 19
        self.sensors.append(Sensor((self.width // 2, 0), (self.height + self.width // 2, self.height)))
        # Backward: len = 19
        self.sensors.append(Sensor((0, self.height // 2), (0, round(
            self.height * 1.5))))  # [5] = [(0, -y) for y in range(self.height // 2, self.height + (self.height // 2))]

    def get_sensor_data(self, city_map):
        """
            Following Input Model plan 4, which is as follows:
            - Each Sensor has 7 verticies for eash of the possibilities (Green light, Dotted line, Yellow Light, Stop Sign,
                Solid Line, Red Light, Car) in that order
            -  It gives the distance to each of those options ( or 0 if not touching )
            - So a total of 6 sensors x 7 verticies = 42 input size
        """
        data = []
        for sensor in self.sensors:
            data += sensor.sense(city_map)
        return data;

    def collision_check(self, otherCar):
        pass

    def display(self, surface):
        """surface is a pygame.Surface object to blit the car onto"""
        if (self.direction == N).all() or (self.direction == S).all():
            pygame.draw.rect(surface, self.color, pygame.Rect(self.topLeft, (self.width, self.height)))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.topLeft, (self.height, self.width)))

        for s in self.sensors:
            s.display(surface, self.pos, self.direction)





class Sensor:
    def __init__(self, startLine, endLine):
        self.start = startLine
        self.end = endLine

    def display(self, surface, carPos, carDir):
        northPos = (
            (self.start[0] + carPos[0], self.start[1] + carPos[1]), (self.end[0] + carPos[0], self.end[1] + carPos[1]))
        rotatedPos = (rotateCoordinate(carPos, northPos[0], carDir), rotateCoordinate(carPos, northPos[1], carDir))
        pygame.draw.line(surface, RED, rotatedPos[0], rotatedPos[1])

    def sense(self, city_map):
        """@:return An array[7] for each possible object to sense (Green light, Dotted line, Yellow Light, Stop Sign,
                Solid Line, Red Light, Car)
        """
        greenLight, yellowLight, redLight, stop = self.get_lights(city_map.intersections)
        dotted, solid = self.get_lines(city_map.roads)
        cars = self.get_cars(city_map.cars)
        return [greenLight, dotted, yellowLight, stop, solid, redLight, cars]

    def get_lights(self, intersections):
        # TODO
        greenLight = 0
        yellowLight = 0
        stop = 0

        # for inter in self.find_touching_intersections(intersections):
        #     if(inter.signal_Type == "stops"):
        #         stop = self.distance()

        return [0,0,0]

    def get_cars(self, cars):
        # TODO
        return 0

    def get_lines(self, roads):
        # TODO
        return [0,0]

    def find_touching_intersections(self, intersections):
        # TODO
        return intersections;


def rotateCoordinate(centerOfRotation, coordinate, direction):
    if (direction == N).all():
        return coordinate
    else:
        x, y = centerOfRotation
        a, b = coordinate
        distance = np.array([x - a, y - b])
        if (direction == S).all():
            rotMat = np.array([[1, 0], [0, 1]])
        elif (direction == W).all():
            rotMat = np.array([[0, -1], [1, 0]])
        elif (direction == E).all():
            rotMat = np.array([[0, 1], [-1, 0]])
        else:
            raise (Exception("Direction Error: ", direction))

        difference = rotMat @ distance
        return difference[0] + centerOfRotation[0], difference[1] + centerOfRotation[1]


def normalizeResult(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    else:
        return -1
