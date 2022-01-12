import car
from pygame.constants import *
from CONSTANTS import *

class manual(car.Car):
    def next_move(self, keys_in=None):
        self.nextMove["pos"] = self.pos
        self.nextMove["velocity"] = self.velocity
        self.nextMove["direction"] = self.direction

        if keys_in[K_UP]:
            self.nextMove["velocity"] = np.array([self.velocity[0] * 1.1, self.velocity[1] * 1.1 ])
        if keys_in[K_DOWN]:
            self.nextMove["velocity"] = np.array([self.velocity[0] * 0.9, self.velocity[1] * 0.9])
        if keys_in[K_LEFT]:
            #fif self.direction == N or self.direction == S:
            self.nextMove["direction"] = rotLeft@self.direction  #(self.direction[1] , self.direction[0])
            self.nextMove["velocity"] = rotLeft@self.velocity  #(self.velocity[1], self.velocity[0])
            #else:
            #    self.nextMove["direction"] = (-self.direction[1], -self.direction[0])
            #    self.nextMove["velocity"] = (-self.velocity[1], -self.velocity[0])
        if keys_in[K_RIGHT]:
            #if self.direction == N or self.direction == S:
            self.nextMove["direction"] = rotRight@self.direction  #(-self.direction[1] , -self.direction[0])
            self.nextMove["velocity"] = rotRight@self.velocity  # (-self.velocity[1], -self.velocity[0])
            #else:
                #self.nextMove["direction"] = (self.direction[1], self.direction[0])
                #self.nextMove["velocity"] = (self.velocity[1], self.velocity[0])






