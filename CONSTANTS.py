WIDTH, HEIGHT = 1200, 800

FPS = 31

# Colors:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (10, 10, 200)

# Directions:
N = (0, -1)  # Turn right is swap * -1; turn left is swap
S = (0, 1)  # Turn right is swap * -1; turn left is swap
W = (-1, 0)  # Turn right is swap, turn left is swap * -1
E = (1, 0)  # Turn right is swap, turn left is swap * -1

# Roads:
LANEWIDTH = 15
LINEWIDTH = 1
DOTTEDLINELENGTH = 5

#SensorValues:
EMPTYROAD = 0
CAR = 1
SOLIDLINE = 2
DOTTEDLINE = 3
GREENLIGHT = 4
YELLOWLIGHT = 5
REDLIGHT = 6
