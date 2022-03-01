"""
Constants used throughout the cityDrivingSim project
"""
import numpy as np

WIDTH, HEIGHT = 1200, 800

FPS = 10

# Colors:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (10, 10, 200)
PINK = (255, 192, 203)

# Directions:
N = np.array([0, -1])  # Turn right is swap * -1; turn left is swap
S = np.array([0, 1])  # Turn right is swap * -1; turn left is swap
W = np.array([-1, 0])  # Turn right is swap, turn left is swap * -1
E = np.array([1, 0])  # Turn right is swap, turn left is swap * -1

NORTH = (0,-1)
SOUTH = (0,1)
WEST = (-1,0)
EAST = (1, 0)

# Roads:
LANEWIDTH = 16
LINEWIDTH = 1
DOTTEDLINELENGTH = 5

CARWIDTH = round(LANEWIDTH * 0.75)  # = about 11 px
CARLENGTH = round(LANEWIDTH * 1.25) # about 19 px

#SensorValues:
EMPTYROAD = 0
CAR = 1
SOLIDLINE = 2
DOTTEDLINE = 3
GREENLIGHT = 4
YELLOWLIGHT = 5
REDLIGHT = 6


# Rotation Matricies:
rotLeft = np.array([[0,1],[-1,0]])
rotRight = np.array([[0, -1],[1, 0]])
