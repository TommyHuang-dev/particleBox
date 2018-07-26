import math
from particle import Particle

class Shockwave:
    # initialize the object
    # start energy = 100 * 10 * 2 = 2000
    def __init__(self, init_pos_x, init_pos_y, init_energy, fake):
        self.startingEnergy = init_energy
        self.currentEnergy = self.startingEnergy
        self.posX = init_pos_x
        self.posY = init_pos_y
        self.fake = fake

        self.radius = 4 + (math.sqrt(self.startingEnergy / 10) / 10)
        self.startingWidth = self.radius / 1.5
        self.width = self.startingWidth
        self.hitList = []

    # grow ring and lower energy
    def expand(self):
        self.radius += 4 + (math.sqrt(self.currentEnergy / 2) / 10)
        self.width = self.width - 0.1
        self.currentEnergy = (self.startingEnergy / (self.radius / 10) ** 2)
        if self.currentEnergy > self.startingEnergy:
            self.currentEnergy = self.startingEnergy
        # make sure width is not below 1
        if self.width < 1:
            self.width = 1
