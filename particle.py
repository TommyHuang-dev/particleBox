from someFunctions import *
import math

# this is simply a program that defines a particle class, used in main.py


# a circle!!
# pos x and y go from top left corner to bottom right corner
# direction is in radians
# velocity is total velocity
# mass is mass :D
# damage increases after collisions, if damage goes above the dmgThreshold, the particle will break apart
# standard particle mass is 100
# particle heals based on its mass, damage, and a base rate
class Particle:
    # initial attributes
    damage = 0
    dmg_threshold = 1
    size = 1

    # initialize the object
    def __init__(self, init_pos_x, init_pos_y, init_vel, init_direction, init_mass):
        # these are defined on particle creation
        self.vel = init_vel
        self.direction = init_direction
        self.posX = init_pos_x
        self.posY = init_pos_y
        self.mass = init_mass

        # based on the defined attributes in __init__
        damage = 0  # starts with minimum damage, gradually lowers to 0 if greater than 0
        self.dmg_threshold = self.calc_threshold()  # explode if damage passes this
        self.size = self.calc_size()  # radius of the particle

    # functions of particle
    def calc_threshold(self):
        return self.mass

    # get radius of particle
    def calc_size(self):
        return math.sqrt(self.mass)

    # returns how much the particle heals
    def calc_heal(self):
        return math.sqrt((self.damage / 200) + (self.mass / 200))

    def update_self(self):
        self.dmgThreshold = self.calc_threshold()
        self.size = self.calc_size()
        self.damage -= self.calc_heal()


# class Test:
#     def __init__(self, val):
#         self.a = val
#     def print_double(self):
#         print(float(self.a) * 2)
