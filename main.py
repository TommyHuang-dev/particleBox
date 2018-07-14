from particle import Particle
from someFunctions import *
import pygame
from pygame import gfxdraw
import time
import sys


# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(0.5)

clock = pygame.time.Clock()
disLength = 1200
disHeight = 800
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("Particle Box")

# colours
backCol = (245, 245, 245)

# test stuff
# testCircle = Particle(init_pos_x=35, init_pos_y=35, init_vel=10, init_direction=90, init_mass=300)
# print(testCircle.calc_size())

# this list holds all particle objects



while True:
    screen.fill(backCol)

    # drawing aa shapes
    # pygame.draw.circle(screen, (50, 200, 50), (testCircle.posX, testCircle.posY), int(testCircle.calc_size() + 1))
    # pygame.gfxdraw.aacircle(screen, testCircle.posX, testCircle.posY, int(testCircle.calc_size()), (0, 0, 0))

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

