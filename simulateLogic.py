# simulateLogic.py
import random
import numpy
import pygame

import manualCar
from car import Car
from road import Road
from intersection import Intersection
from CONSTANTS import *


class CityMap:
    def __init__(self, layout: "default or custom?" = "default", driving_mode: "manual or autoPopulate?" = "autoPopulate"):
        self.cars = []
        self.roads = []
        self.intersections = []
        # self.qRES = 0

        if layout == "default":  # Will show chicago style roads
            self.roads.append(
                Road((0, HEIGHT - LANEWIDTH * 5), (WIDTH, HEIGHT - LANEWIDTH * 5), 8, E))  # Bottom Big Road 8 lanes
            self.roads.append(Road((LANEWIDTH * 4, 0), (LANEWIDTH * 4, HEIGHT), 6, S))  # Left big 6 lane road
            self.roads.append(
                Road((WIDTH - LANEWIDTH * 5, 0), (WIDTH - LANEWIDTH * 5, HEIGHT), 8, S))  # Right big road 8 lanes
            self.roads.append(Road((0, LANEWIDTH * 3), (WIDTH, LANEWIDTH * 3), 4, E))  # Top Road 4 lanes
            self.roads.append(
                Road((WIDTH // 2, LANEWIDTH * 3), (WIDTH // 2, HEIGHT - LANEWIDTH), 4, S))  # Middle 4 lane road
            for qq in range(3):  # Small E-W streets
                self.roads.append(Road((LANEWIDTH * 3, LANEWIDTH * 10 + qq * WIDTH // 10),
                                       (WIDTH - LANEWIDTH, LANEWIDTH * 10 + qq * WIDTH // 10), 2, E))

            self.roads.append(Road((WIDTH // 4, LANEWIDTH * 10),
                                   (WIDTH // 4, LANEWIDTH * 11 + 2 * WIDTH // 10), 2, S))

            for e, r in enumerate(self.roads):  # This does
                for r2 in self.roads[e:]:
                    signal_type = "stops" if r.num_lanes + r2.num_lanes <= 6 else "lights"
                    try:
                        if (r.direction == N).all() or (r.direction == S).all():
                            I = Intersection(r, r2, signal_type)
                        else:
                            I = Intersection(r2, r, signal_type)
                    except ValueError:  # the roads don't intersect
                        pass
                    else:
                        self.intersections.append(I)

            self.initialize_cars(driving_mode)


    def initialize_cars(self, driving_mode):
        if driving_mode == "autoPopulate":
            for road in self.roads:
                if (road.direction == N).all() or (road.direction == S).all():
                    self.cars.append(Car((road.start[0] - LANEWIDTH // 2 + LINEWIDTH * 2, road.start[1]), direction=road.direction))
                else:
                    self.cars.append(Car((road.start[0], road.start[1] - LANEWIDTH // 2 + LINEWIDTH * 2), direction=road.direction))

        elif driving_mode == "manual":
            self.cars.append(manualCar.manual((40,40)))

    def check_pixel(self, x, y):
        """Finds at Position(x,y) what is there on the map"""
        return 0  # Value 0-6 sensorValue

    def update_frame(self, keyMap=None):  # TESTING, qFrameNum):
        for car in self.cars:
            if keyMap == None:
                car.next_move()  # TESTING result=[self.qRES, self.qRES, self.qRES])
            else:
                car.next_move(keyMap)
        for car in self.cars:
            car.update(False) # Testing: put in collision check
        for intersect in self.intersections:
            if intersect.signalType == "lights":
                r = random.randint(0, 100)
                if r > 99:  # 1 % chance on the frame that the light will change
                    intersect.swap_signal_state()
        # Testing
        '''
        if self.qRES == 1:
            self.qRES = 0
        if qFrameNum == 60:
            self.qRES = 1
        '''

    def display(self, surface):
        for road in self.roads:
            road.display(surface)
        for i in self.intersections:
            i.display(surface)
        for car in self.cars:
            car.display(surface)

        return 0
