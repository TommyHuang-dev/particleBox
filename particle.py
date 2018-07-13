from someFunctions import *

# this is simply a program that defines a particle class, used in main.py


# needed attributes:
# x and y velocity
# if there is x and y velocities u dont need this

class Particle:
    def __init__(self, init_pos_x, init_pos_y, init_vel_x, init_vel_y):
        self.velX = init_vel_x
        self.velY = init_vel_y
        self.posX = init_pos_x
        self.posY = init_pos_y
        # add later
        # self.totalVel =
        pass
    pass

class Test:
    def __init__(self, val):
        self.a = val
    def print_double(self):
        print(float(self.a) * 2)

