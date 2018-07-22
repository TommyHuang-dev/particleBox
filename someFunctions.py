import math

# this program has many useful functions that are used in other programs

# takes in the x y vel and converts to an angle (radians) using dat trig
# returns [angle, velocity]
def xyVel_to_angVel(xy_velocities):
    return math.atan2(-(xy_velocities[1]), xy_velocities[0]), math.sqrt(xy_velocities[0] ** 2 + xy_velocities[1] ** 2)

# takes in a angle (radians) and velocity and converts it into x velocity and y velocity
# returns [xVelocity, yVelocity]
def angVel_to_xy(angle, velocity):
    return (velocity * math.cos(angle)), (velocity * - math.sin(angle))

# PYTHAGOREAN THEOREM YAY
def calc_hypotenuse(xDiff, yDiff):
    return math.sqrt(xDiff ** 2 + yDiff ** 2)


