from particle import Particle
from shockwave import Shockwave
from someFunctions import *
import pygame
from pygame import gfxdraw
import random
import time
import sys

# TODO: circles are displayed, they effect eachother using gravity
# TODO: they can collide with eachother and explode
# TODO: wobbly particles if they are on the brink of exploding


# this function breaks a particle apart if it takes too much damage
def split(particle, list):
    # small particles cannot be destroyed
    if particle.mass <= 20:
        particle.damage = particle.dmgThreshold - 1
        return

    # init_pos_x, init_pos_y, init_vel, init_direction, init_mass
    abs_excess = particle.damage - particle.calc_threshold()  # e.g. 1200dmg, 1000threshold = 200 abs_excess
    per_excess = abs_excess / particle.calc_threshold()  # e.g. 1200dmg, 1000threshold = 0.2 per_excess

    # more damaged objects spawn moar
    num_spawned = random.randint(int(per_excess * 3) + 1,
                                 int(per_excess * 5) + 2)
    if num_spawned < 1:
        num_spawned = 1

    for i in range(num_spawned):
        # ejection mass increases with lower spawn number and higher excess
        ejection_mass = random.randint(int(abs_excess / num_spawned * 0.15),
                                       int(abs_excess / num_spawned * 1.0))
        # make sure ejection mass doesn't exceed 1/3 of the object's mass or is too low
        if ejection_mass * 3 > particle.mass:
            ejection_mass = int(particle.mass / 3)

        if ejection_mass < 10:
            particle.damage -= (abs_excess + 1)
            break

                # decrease the main particle's mass and damage
        particle.mass -= ejection_mass
        particle.damage -= ejection_mass * 2 + abs_excess / 10
        particle.update_self()

        # random angle that the particle will be ejected from
        ejection_force = random.randint(int(ejection_mass * 15.0 * (per_excess * 1.0 + 1) + math.sqrt(abs_excess) * 0.05),
                                        int(ejection_mass * 20.0 * (per_excess * 1.4 + 1) + math.sqrt(abs_excess) * 0.05))
        ejection_angle = random.uniform(0, math.pi * 2)

        # apply the forces
        init_pos = angVel_to_xy(ejection_angle, particle.calc_size() * 1.1 + 2)
        init_vel = ejection_force / ejection_mass

        # create new particle, apply force to old particle
        new_particle = Particle(particle.posX + init_pos[0], particle.posY +
                                init_pos[1], init_vel, ejection_angle, ejection_mass, particle.type)
        new_particle.invul = 15  # invulnerable for 0.1s so it doesnt instantly recombine
        new_particle.damage = random.uniform(new_particle.calc_threshold() * 0.4, new_particle.calc_threshold() * 0.8)
        particle.apply_force(ejection_force, ejection_angle + math.pi)

        # add to list
        list.append(new_particle)

        # recalculating...
        abs_excess = particle.damage - particle.calc_threshold()
        per_excess = abs_excess / particle.calc_threshold()

        # when particle recovers, break loop
        if abs_excess < 0:
            break


# given two masses and their x y coords,, this function finds their center of mass
def find_center_of_mass(particle1, particle2):
    xy_diff = [particle1.posX - particle2.posX, particle1.posY - particle2.posY]
    mass_diff = particle2.mass / (particle1.mass + particle2.mass)
    center_pos = [particle1.posX - (xy_diff[0] * mass_diff), particle1.posY - (xy_diff[1] * mass_diff)]
    return center_pos

# find the average x y without weighting the mass
def find_center(particle1, particle2):
    xy_diff = [particle1.posX - particle2.posX, particle1.posY - particle2.posY]
    ratio = particle1.size / (particle1.size + particle2.size)
    center_pos = [particle1.posX - (xy_diff[0] * ratio),
                  particle1.posY - (xy_diff[1] * ratio)]

    return center_pos

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

# this list holds all particle and shockwave objects
particleList = []
shockwaveList = []

# constants
GRAVITY_CONST = 400

# create new particles
newParticleSize = 100
newParticleType = "matter"  # matter or antimatter

# USER EXPERIENCE :D (UI)
sizeFont = pygame.font.SysFont('Courier New', 20)

# user controls
buttonPressed = False
selectedPos = [0, 0]
changeSizeDelay = [0, 5]
cameraSpeed = 5

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
        if timeAccel < 0.25:
            timeAccel = 0.25

    # create new particles
    # left click = matter, right click = antimatter
    mouse = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    # set location
    if not buttonPressed:
        if mouse[0] == 1:
            newParticleType = "matter"
            buttonPressed = True
            selectedPos = mousePos
        elif mouse[2] == 1:
            newParticleType = "antimatter"
            buttonPressed = True
            selectedPos = mousePos

    # set velocity and initialize particle on release
    if buttonPressed and mouse[0] == 0 and mouse[2] == 0:
        buttonPressed = False
        # handle velocities and angles here:
        distance = math.sqrt((selectedPos[0] - mousePos[0]) ** 2 + (selectedPos[1] - mousePos[1]) ** 2)
        initVel = distance / 2
        initAngle = math.atan2(-(selectedPos[1] - mousePos[1]), selectedPos[0] - mousePos[0])

        # instantiate!!! very exciting!!! waow
        newlyCreatedParticle = Particle(selectedPos[0], selectedPos[1], initVel, initAngle, newParticleSize, newParticleType)
        particleList.append(newlyCreatedParticle)

    # otherwise, draw a outline/preview
    elif buttonPressed and (mouse[0] == 1 or mouse[2] == 1):
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
        for i in range(len(shockwaveList)):
            shockwaveList[i].posX += - cam_move[0]
            shockwaveList[i].posY += - cam_move[1]

    # check for collisions, break them up if too much damage is taken
    i = 0

    while i < len(particleList):
        j = i + 1
        while j < len(particleList):
            # get change in x and y and distance
            diff = (particleList[i].posX - particleList[j].posX), (particleList[i].posY - particleList[j].posY)
            distance = math.sqrt(diff[0] ** 2 + diff[1] ** 2)

            if distance < (particleList[i].calc_size() + particleList[j].calc_size() + 1) * 0.99 and \
                    particleList[i].invul <= 0 and particleList[j].invul <= 0:

                # collision for two particles of same type
                if particleList[i].type == particleList[j].type:
                    # calculate collision velocity for damage
                    velocity1 = angVel_to_xy(particleList[i].direction, particleList[i].vel)
                    velocity2 = angVel_to_xy(particleList[j].direction, particleList[j].vel)
                    collVel = [velocity1[0] - velocity2[0], velocity1[1] - velocity2[1]]

                    # 1/2 mv^2
                    totalFinalVel = calc_hypotenuse(collVel[0], collVel[1])
                    impactDamage = (totalFinalVel / 10) ** 2 * min([particleList[i].mass, particleList[j].mass]) / 100

                    # calculate the initial velocity of the new particle (total velocity / mass)
                    initialXVel = velocity1[0] * particleList[i].mass + velocity2[0] * particleList[j].mass
                    initialYVel = velocity1[1] * particleList[i].mass + velocity2[1] * particleList[j].mass

                    travellingAngVel = xyVel_to_angVel([initialXVel, initialYVel])

                    # create a new particle, based on the speeds of the two colliding particles and
                    # their center of masses
                    centerOfMassXY = find_center_of_mass(particleList[i], particleList[j])
                    newParticle = Particle(centerOfMassXY[0],
                                           centerOfMassXY[1],
                                           travellingAngVel[1] / (particleList[i].mass + particleList[j].mass),
                                           travellingAngVel[0],
                                           particleList[i].mass + particleList[j].mass,
                                           particleList[i].type)

                    # update all attributes
                    newParticle.update_self()
                    newParticle.damage = particleList[i].damage + particleList[j].damage + impactDamage

                    # fake shockwave on higher energy collisions
                    if impactDamage > 30:
                        # CREATE A FAKE SMALL SHOCKWAVE FOR VISUAL EFFECT
                        # calculate mass loss and the energy released based on the smaller of the two particles
                        shockwaveXY = find_center(particleList[i], particleList[j])

                        newShockwave = Shockwave(shockwaveXY[0], shockwaveXY[1], impactDamage / 3, True)
                        shockwaveList.append(newShockwave)

                    # delete old particles, start new one
                    particleList[j] = newParticle
                    del (particleList[i])

                # collision for anti-matter / matter particles (EXPLOSION!!)
                elif particleList[i].type != particleList[j].type:
                    # calculate mass loss and the energy released based on the smaller of the two particles
                    massLoss = min(particleList[i].mass, particleList[j].mass)
                    energyRelease = massLoss * 16 * 2
                    xyDiff = [particleList[i].posX - particleList[j].posX, particleList[i].posY - particleList[j].posY]
                    shockwaveXY = find_center(particleList[i], particleList[j])

                    # generate a new shockwave!! SPOOKY
                    newShockwave = Shockwave(shockwaveXY[0], shockwaveXY[1], energyRelease, False)
                    shockwaveList.append(newShockwave)

                    # cause particles to lose mass
                    particleList[i].mass -= massLoss
                    particleList[j].mass -= massLoss
                    # delete the particles if mass gets too low
                    if particleList[j].mass < 10:
                        del(particleList[j])
                    else:
                        particleList[j].damage += energyRelease / 4
                    if particleList[i].mass < 10:
                        del(particleList[i])
                    else:
                        particleList[i].damage += energyRelease / 4

            j += 1

        i += 1

    # create new particles from damaged one
    for i in range(len(particleList)):
        if particleList[i].damage > particleList[i].dmgThreshold:
            split(particleList[i], particleList)

    # apply forces and move each particle
    for i in range(len(particleList)):
        # update particle stats like damage
        particleList[i].update_self()
        # accelerate particle based on gravity
        for j in range(i + 1, len(particleList), 1):
            # get change in x and y and distance
            if particleList[i].invul <= 0 and particleList[j].invul <= 0:
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

        if particleList[i].calc_size() + wobble < 2:
            wobble = particleList[i].calc_size() * 0.8

        # draw on screen
        pygame.gfxdraw.filled_circle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                     int(particleList[i].calc_size() + wobble), particleList[i].calc_colour())
        pygame.gfxdraw.aacircle(screen, int(particleList[i].posX), int(particleList[i].posY),
                                int(particleList[i].calc_size() + wobble), particleList[i].calc_line_colour())

    # check for collisions with shockwave
    for i in range(len(shockwaveList)):
        # so many nested statements :O
        if not shockwaveList[i].fake:
            for j in range(len(particleList)):
                # make sure the particle doesnt get hit by the same shockwave twice
                if particleList[j] not in shockwaveList[i].hitList:
                    distance = calc_hypotenuse(shockwaveList[i].posX - particleList[j].posX,
                                           shockwaveList[i].posY - particleList[j].posY)
                    minDistance = shockwaveList[i].radius + particleList[j].size * 0.95 + 1
                    # check if the shockwave reaches the particle
                    if shockwaveList[i].radius / 2 - 50 < distance < minDistance:
                        xyDiff = [shockwaveList[i].posX - particleList[j].posX,
                                  shockwaveList[i].posY - particleList[j].posY]
                        # deal damage and apply a force
                        shockwaveList[i].hitList.append(particleList[j])
                        particleList[j].damage += shockwaveList[i].currentEnergy
                        particleList[j].apply_force(((shockwaveList[i].currentEnergy / 2) * 10 * (particleList[j].size / 8)),
                                                    math.atan2(-xyDiff[1], xyDiff[0]) + math.pi)

    # draw and expand shockwave
    i = 0
    while i < len(shockwaveList):
        # draw a not anti-aliased circle
        colDiff = 40 * shockwaveList[i].width / shockwaveList[i].startingWidth
        if shockwaveList[i].fake:
            pygame.draw.circle(screen, (225 - colDiff * 2, 225 - colDiff * 2, 225 - colDiff * 2),
                               (int(shockwaveList[i].posX), int(shockwaveList[i].posY)),
                               int(shockwaveList[i].radius), int(shockwaveList[i].width + 0.6))
        else:
            pygame.draw.circle(screen, (120, 130 + colDiff * 2.25, 150 + colDiff * 2.5),
                               (int(shockwaveList[i].posX), int(shockwaveList[i].posY)),
                               int(shockwaveList[i].radius), int(shockwaveList[i].width + 0.6))

        # IT GROWS!!! :O
        # print(int(shockwaveList[i].width + 0.6))
        shockwaveList[i].expand()
        # delete shockwave if its energy is too low
        if shockwaveList[i].currentEnergy < 10:
            del (shockwaveList[i])

        i += 1

    # garbage collection!!! Removes particles that fly too far, also counts down invulnerability
    for i in range(len(particleList)):
        particleList[i].invul -= 1
        # garbage collection!!! If a particle is super far away, delete it
        if not -5000 < particleList[i].posX < disLength + 5000 or \
                not -5000 < particleList[i].posY < disHeight + 5000:
            del (particleList[i])
            break

    # UI elements
    # display the size of newly created particles
    size_text = sizeFont.render("mass: " + str(newParticleSize), False, (0, 0, 0))
    screen.blit(size_text, (30, disHeight - 50))

    # display time warp!!
    if timeAccel >= 1:
        time_text = sizeFont.render("time scale: " + str(int(timeAccel)) + "x", False, (0, 0, 0))
    else:
        time_text = sizeFont.render("time scale: " + str(round(timeAccel, 2)) + "x", False, (0, 0, 0))
    screen.blit(time_text, (30, disHeight - 100))

    # update display!
    pygame.display.update()

    # should make it 60FPS max
    clock.tick(int(60 * timeAccel))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
