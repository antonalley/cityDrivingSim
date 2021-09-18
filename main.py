# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from simulateLogic import *
import sys
from pygame.locals import QUIT

#Test git
def main():
    thismap = CityMap()
    DISPLAY = pygame.display.set_mode((1200, 800), 0, 32)
    pygame.init()

    while True:
        temp_surf = pygame.Surface((WIDTH, HEIGHT))
        temp_surf.fill(GRAY)
        thismap.display(temp_surf)
        DISPLAY.blit(temp_surf, (0, 0))
        pygame.display.set_caption(str(pygame.mouse.get_pos()))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        del temp_surf


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
