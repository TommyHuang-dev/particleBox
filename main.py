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
    print("boom")
    pass


# setup pygame
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disLength = 1400
disHeight = 800
screen = pygame.display.set_mode((disLength, disHeight))
pygame.display.set_caption("Particle Box")

# colours
backCol = (245, 245, 245)

# this list holds all particle objects
particleList = []

# constants
GRAVITY_CONST = 300

# create new particles
newParticleSize = 100

# USER EXPERIENCE :D (UI)
sizeFont = pygame.font.SysFont('Courier New', 20)

# user controls
buttonPressed = False
selectedPos = [0, 0]
changeSizeDelay = [0, 5]
cameraSpeed = 4

timeAccel = 1
changeAccelDelay = [0, 10]

while True:
    screen.fill(backCol)

    # change size of newly created particles
    changeSizeDelay[0] -= 1 * (1 / timeAccel)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_r] and changeSizeDelay[0] <= 0:
        newParticleSize += 10
        changeSizeDelay[0] = changeSizeDelay[1]
    elif pressed[pygame.K_f] and changeSizeDelay[0] <= 0:
        newParticleSize -= 10
        changeSizeDelay[0] = changeSizeDelay[1]
    elif pressed[pygame.K_t] and changeSizeDelay[0] <= 0:
        newParticleSize += 100
        changeSizeDelay[0] = changeSizeDelay[1]
    elif pressed[pygame.K_g] and changeSizeDelay[0] <= 0:
        newParticleSize -= 100
        changeSizeDelay[0] = changeSizeDelay[1]

    if newParticleSize <= 10:
        newParticleSize = 10

    # speed up or slow down time
    changeAccelDelay[0] -= 1 * (1 / timeAccel)
    if pressed[pygame.K_e] and changeAccelDelay[0] <= 0:  # speed up
        timeAccel *= 2
        changeAccelDelay[0] = changeAccelDelay[1]
        if timeAccel > 4:
            timeAccel = 4
    elif pressed[pygame.K_q] and changeAccelDelay[0] <= 0:  # slow down
        timeAccel *= 0.5
        changeAccelDelay[0] = changeAccelDelay[1]
        if timeAccel < 0.5:
            timeAccel = 0.5

    # create new particles
    mouse = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    # set location
    if mouse[0] == 1 and not buttonPressed:
        buttonPressed = True
        selectedPos = mousePos

    # set velocity and initialize particle on release
    if buttonPressed and mouse[0] == 0:
        buttonPressed = False
        # handle velocities and angles here:
        distance = math.sqrt((selectedPos[0] - mousePos[0]) ** 2 + (selectedPos[1] - mousePos[1]) ** 2)
        initVel = distance / 4
        initAngle = math.atan2(-(selectedPos[1] - mousePos[1]), selectedPos[0] - mousePos[0])

        # instantiate!!! very exciting!!! waow
        newlyCreatedParticle = Particle(selectedPos[0], selectedPos[1], initVel, initAngle, newParticleSize)
        particleList.append(newlyCreatedParticle)

    # otherwise, draw a outline/preview
    elif buttonPressed and mouse[0] == 1:
        pygame.draw.line(screen, (100, 50, 0), mousePos, selectedPos)
        pygame.gfxdraw.aacircle(screen, selectedPos[0], selectedPos[1],
                                int(math.sqrt(newParticleSize)), (0, 0, 0))

    # camera movement
    cam_move = [0, 0]
    if pressed[pygame.K_w]:  # up
        cam_move[1] = - cameraSpeed
    elif pressed[pygame.K_s]:  # down
        cam_move[1] = cameraSpeed
    if pressed[pygame.K_a]:  # left
        cam_move[0] = - cameraSpeed
    elif pressed[pygame.K_d]:  # right
        cam_move[0] = cameraSpeed

    if cam_move != [0, 0]:
        for i in range(len(particleList)):
            particleList[i].posX += - cam_move[0]
            particleList[i].posY += - cam_move[1]

    # check for collisions, break them up if too much damage is taken
    i = 0
    while i < len(particleList):
        j = i + 1
        while j < len(particleList):
            # get change in x and y and distance
            diff = (particleList[i].posX - particleList[j].posX), (particleList[i].posY - particleList[j].posY)
            distance = math.sqrt(diff[0] ** 2 + diff[1] ** 2)

            if distance < (particleList[i].calc_size() + particleList[j].calc_size() + 1) * 0.95:
                # calculate collision velocity for damage
                velocity1 = angVel_to_xy(particleList[i].direction, particleList[i].vel)
                velocity2 = angVel_to_xy(particleList[j].direction, particleList[j].vel)
                collVel = [velocity1[0] - velocity2[0], velocity1[1] - velocity2[1]]

                # 1/2 mv^2
                totalFinalVel = calc_hypotenuse(collVel[0], collVel[1])
                impactDamage = ((totalFinalVel / 50) ** 2 * (particleList[i].mass + particleList[j].mass)) / 40
                print(impactDamage)

                # calculate the initial velocity of the new particle (total velocity / mass)
                initialXVel = velocity1[0] * particleList[i].mass + velocity2[0] * particleList[j].mass
                initialYVel = velocity1[1] * particleList[i].mass + velocity2[1] * particleList[j].mass

                travellingAngVel = xyVel_to_angVel([initialXVel, initialYVel])

                # create a new particle, based on the speeds of the two colliding particles
                newParticle = Particle(particleList[i].posX - (
                diff[0] * particleList[j].mass / (particleList[i].mass + particleList[j].mass)),
                                       particleList[i].posY - (diff[1] * particleList[j].mass / (
                                       particleList[i].mass + particleList[j].mass)),
                                       travellingAngVel[1] / (particleList[i].mass + particleList[j].mass),
                                       travellingAngVel[0],
                                       particleList[i].mass + particleList[j].mass)

                # update all attributes
                newParticle.update_self()
                newParticle.damage = particleList[i].damage + particleList[j].damage + impactDamage
                # delete old particles, start new one
                particleList[j] = newParticle
                del (particleList[i])
            j += 1

        i += 1
        # create new particles from damaged one
        # if particleList[i].damage > particleList[i].dmgThreshold:
        # explode(particleList[i], particleList)

    # apply forces and move each particle
    for i in range(len(particleList)):
        # update particle stats like damage
        particleList[i].update_self()
        # accelerate particle based on gravity
        for j in range(i + 1, len(particleList), 1):
            # get change in x and y and distance
            diff = (particleList[i].posX - particleList[j].posX), (particleList[i].posY - particleList[j].posY)
            distance = calc_hypotenuse(diff[0], diff[1])

            # equation for force of gravity:
            # gravitational constant * (mass1 + mass2) / distance^2 / 60 ticks per second
            try:
                gravity_force = GRAVITY_CONST * ((particleList[i].mass * particleList[j].mass) / distance ** 2) / 30
                gravity_direction = math.atan2(-diff[1], diff[0])
            except ZeroDivisionError:
                gravity_force = 0
                gravity_direction = 0

            # apply the FORCE
            particleList[i].apply_force(gravity_force, gravity_direction + math.pi)
            particleList[j].apply_force(gravity_force, gravity_direction)

        # movement of the particle
        particleList[i].move()

    # display the particles, add special effects
    for i in range(len(particleList)):
        # vibrate particles if they take too much damage
        wobble = random.uniform(-math.sqrt(particleList[i].damage) / 25, math.sqrt(particleList[i].damage) / 25)

        # draw on screen
        try:
            pygame.gfxdraw.filled_circle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                         int(particleList[i].calc_size() + wobble), particleList[i].calc_colour())
            pygame.gfxdraw.aacircle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                    int(particleList[i].calc_size() + wobble), (0, 0, 0))
        except TypeError:
            pygame.gfxdraw.filled_circle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                         int(particleList[i].calc_size() + wobble), (250, 0, 50))
            pygame.gfxdraw.aacircle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                    int(particleList[i].calc_size() + wobble), (0, 0, 0))

    # garbage collection!!! Removes particles that fly too far
    for i in range(len(particleList)):
        # garbage collection!!! If a particle is super far away, delete it
        if not -10000 < particleList[i].posX < disLength + 10000 or \
                not -10000 < particleList[i].posY < disHeight + 10000:
            del (particleList[i])
            break

    # UI elements
    # display the size of newly created particles
    size_text = sizeFont.render("size: " + str(newParticleSize), False, (0, 0, 0))
    screen.blit(size_text, (30, disHeight - 50))

    # display time warp!!
    if timeAccel >= 1:
        time_text = sizeFont.render("time scale: " + str(int(timeAccel)) + "x", False, (0, 0, 0))
    else:
        time_text = sizeFont.render("time scale: " + str(round(timeAccel, 1)) + "x", False, (0, 0, 0))
    screen.blit(time_text, (30, disHeight - 100))

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(int(60 * timeAccel))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

