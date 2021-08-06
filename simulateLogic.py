# simulateLogic.py

class CityMap:
    def __init__(self):
        self.cars = []
        self.roads = []
        self.intersections = []

    def check_pixel(self, x, y):
        """Finds at Position(x,y) what is there on the map"""
        return 0  # Value 0-6 sensorValue

    class Road:
        def __init__(self):
            None

    class Intersection:
        def __init__(self):
            None


class Car:
    def __init__(self):
        self.nextMove = []
        self.pos = (0, 0)  # The center of the car

    def next_move(self):
        """Takes the current state of game and determines what the next move will be, without making any changes yet"""
        result = 0  # Temporary- do the calculations here
        self.nextMove = result
        return 0;

    def update(self):
        """puts the next move into action"""
        return None

    def generate_sensors(self):
        """returns list of every sensor with every x,y coordinate in it"""
        return []
