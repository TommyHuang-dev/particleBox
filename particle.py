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
    dmgThreshold = 1
    size = 1
    invul = 0  # invulnerability frames

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
        self.dmgThreshold = self.calc_threshold()  # explode if damage passes this
        self.size = self.calc_size()  # radius of the particle

    # functions of particle
    def calc_threshold(self):
        return (self.mass ** 1.04) + 5

    # get radius of particle
    def calc_size(self):
        return math.sqrt(self.mass)

    def calc_colour(self):
        visual_dmg = int(self.damage / self.dmgThreshold * 200)
        return 100 + int(visual_dmg * 0.75), 100 - int(visual_dmg * 0.4), 100 - int(visual_dmg * 0.4)

    # returns how much the particle heals
    def calc_heal(self):
        return math.sqrt(self.damage / 300) + math.sqrt(self.dmgThreshold / 600)

    def update_self(self):
        self.dmgThreshold = self.calc_threshold()
        self.size = self.calc_size()
        self.damage -= self.calc_heal()
        self.invul -= 1
        if self.damage < 0:
            self.damage = 0

    def move(self):
        change = angVel_to_xy(self.direction, self.vel)
        self.posX += change[0] / 20
        self.posY += change[1] / 20

    # applies a force to the object before mass is included
    def apply_force(self, magnitude, force_direction):
        force_effect = magnitude / self.mass
        # get the change in xy_vel
        initial_xy_vel = list(angVel_to_xy(self.direction, self.vel))
        change_xy_vel = list(angVel_to_xy(force_direction, force_effect))
        initial_xy_vel[0] += change_xy_vel[0]
        initial_xy_vel[1] += change_xy_vel[1]

        # re-convert back to angle + velocity
        new_angvel = xyVel_to_angVel(initial_xy_vel)
        self.vel = new_angvel[1]
        self.direction = new_angvel[0]

