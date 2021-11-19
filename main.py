import time

import pygame

from simulateLogic import *
import sys
from pygame.locals import QUIT

# TODO:: Get rid of variables that start with 'q' - these were meant to be temporary

def main():
    thismap = CityMap()
    DISPLAY = pygame.display.set_mode((1200, 800), 0, 32)
    pygame.init()
    pause = False
    gameClock = pygame.time.Clock()
    qFrameNum = 0
    while True:
        if not pause:
            thismap.update_frame(qFrameNum)
            DISPLAY.fill(GRAY)
            thismap.display(DISPLAY)
            pygame.display.set_caption(str(pygame.mouse.get_pos()))
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pause = False

        qFrameNum += 1
        gameClock.tick(FPS)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
