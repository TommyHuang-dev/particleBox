from particle import Particle
from someFunctions import *
import pygame
from pygame import gfxdraw
import random
import time
import sys

# TODO: circles are displayed, they effect eachother using gravity
# TODO: they can collide with eachother and explode
# TODO: wobbly particles if they are on the brink of exploding


def explode(particle, list):
    pass

# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disLength = 1200
disHeight = 800
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("Particle Box")

# colours
backCol = (245, 245, 245)

# this list holds all particle objects
particleList = []

# constants
GRAVITY_CONST = 10000

# test stuff, delete later!!
testCircle1 = Particle(init_pos_x=400, init_pos_y=400, init_vel=35, init_direction=math.pi/2, init_mass=50)
particleList.append(testCircle1)
testCircle2 = Particle(init_pos_x=600, init_pos_y=400, init_vel=0, init_direction=0, init_mass=3000)
particleList.append(testCircle2)
#testCircle3 = Particle(init_pos_x=700, init_pos_y=300, init_vel=10, init_direction=math.pi/2*3, init_mass=500)
#particleList.append(testCircle3)

while True:
    screen.fill(backCol)

    # apply forces and move each particle
    for i in range(len(particleList)):
        # update particle stats like damage
        particleList[i].update_self()
        # accelerate particle based on gravity
        for j in range(i + 1, len(particleList), 1):
            # get change in x and y and distance
            diff = (particleList[i].posX - particleList[j].posX), (particleList[i].posY - particleList[j].posY)
            distance = math.sqrt(diff[0] ** 2 + diff[1] ** 2)

            # equation for force of gravity:
            # gravitational constant * (mass1 + mass2) / distance^2 / 60 ticks per second
            gravity_force = GRAVITY_CONST * ((particleList[i].mass + particleList[j].mass) / distance ** 2) / 30
            gravity_direction = math.atan2(-diff[1], diff[0])

            # apply the FORCE
            particleList[i].apply_force(gravity_force, gravity_direction + math.pi)
            particleList[j].apply_force(gravity_force, gravity_direction)

        # movement of the particle
        particleList[i].move()

    # check for collisions, break them up if too much damage is taken
    for i in range(len(particleList)):

        # create new particles from damaged one
        if particleList[i].damage > particleList[i].dmgThreshold:
            explode(particleList[i], particleList)

    # display the particles, add special effects
    for i in range(len(particleList)):
        # vibrate particles if they take too much damage
        wobble = random.uniform(-math.sqrt(particleList[i].damage) / 25, math.sqrt(particleList[i].damage) / 25)

        # draw on screen
        pygame.gfxdraw.filled_circle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                     int(particleList[i].calc_size() + wobble), particleList[i].calc_colour())
        pygame.gfxdraw.aacircle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                int(particleList[i].calc_size() + wobble), (0, 0, 0))

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

