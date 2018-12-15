import math
from particle import Particle

class Shockwave:
    # initialize the object
    # start energy = 100 * 10 * 2 = 2000
    def __init__(self, init_pos_x, init_pos_y, init_energy, fake):
        self.startingEnergy = init_energy  # collision energy
        self.currentEnergy = self.startingEnergy
        self.posX = init_pos_x
        self.posY = init_pos_y
        self.fake = fake
        self.radius = 5 + ((self.startingEnergy / 4) ** 0.4)
        self.startingWidth = self.radius / 4
        self.width = self.startingWidth
        self.hitList = []

        # update starting energy
        self.currentEnergy = 5 * (self.startingEnergy / ((self.radius / 4) ** 2))

    # grow ring and lower energy
    def expand(self):
        self.radius += 5 + (math.sqrt(self.currentEnergy / 5) / 2)
        self.width = (self.width * 0.99 - 0.2)
        self.currentEnergy = 5 * (self.startingEnergy / ((self.radius / 4) ** 2))
        # debug :P
        if self.currentEnergy > self.startingEnergy:
            self.currentEnergy = self.startingEnergy
        # make sure width is not below 1
        if self.width < 1:
            self.width = 1
