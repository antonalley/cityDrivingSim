"""
Run this file to drive one car through the streets
Use Arrow keys to direct
"""

# TODO: and maybe to collect data and to train the car


import time

import pygame

from simulateLogic import *
import sys
from pygame.locals import QUIT

def main():
    thismap = CityMap(driving_mode="manual")
    keyMap = {pygame.K_DOWN:False, pygame.K_UP:False, pygame.K_LEFT:False, pygame.K_RIGHT:False}
    DISPLAY = pygame.display.set_mode((1200, 800), 0, 32)
    pygame.init()
    pause = False
    gameClock = pygame.time.Clock()
    qFrameNum = 0
    while True:
        if not pause:
            thismap.update_frame(keyMap)
            DISPLAY.fill(GRAY)
            thismap.display(DISPLAY)
            pygame.display.set_caption(str(pygame.mouse.get_pos()))
            pygame.display.flip()

        # Reset the keymap so the car doesn't keep turning
        for key in keyMap:
            keyMap[key] = False

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
                elif event.key in keyMap:
                    keyMap[event.key] = True

        qFrameNum += 1
        gameClock.tick(FPS)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
