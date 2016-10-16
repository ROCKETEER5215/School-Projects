import pygame
from math3d import *
from objects3d import *
import raytracer

# Pygame setup
pygame.display.init()
screen = pygame.display.set_mode((300,200))
done = False
currentLine = 0

# Raytracer setup
RT = raytracer.Raytracer(screen, VectorN((1, 1, 1)))
# Plane
RT.mObjects.append(Plane(VectorN((0, 1, 0)), 0, \
        Material(VectorN((0.3, 0.3, 0)), VectorN((1, 1, 0)), VectorN((0.5, 0.5, 0.5)), 10)))
# Sphere
RT.mObjects.append(Sphere(VectorN((0, 0, 0)), 10, \
        Material(VectorN((0.3, 0, 0)), VectorN((1, 0, 0)), VectorN((1, 1, 1)), 15)))
# AABB
RT.mObjects.append(AABB(VectorN((25, 5, 0)), VectorN((40, 25, 20)), \
        Material(VectorN((0, 3.0, 0)), VectorN((0,1,0)), VectorN((0, 1, 1)), 5)))
# CylinderY
RT.mObjects.append(CylinderY(VectorN((-17, 6, 30)), 22.0, 15.0, \
        Material(VectorN((0.1, 0.1, 0.3)), VectorN((0.7,0.7,1)), VectorN((1, 0, 1)), 20)))
# Camera
RT.setCamera(VectorN((0, 8, -50)), VectorN((0, 0, 0)), VectorN((0, 1, 0)), 60.0, 1.0)
# Light
RT.mLights.append(PointLight(VectorN((0, 25, 0)), VectorN((0.5, 1, 1)), VectorN((1, 1, 1))))
while not done:
    # Input
    eList = pygame.event.get()
    for e in eList:
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            done = True

    # Draw
    if currentLine < screen.get_height():
        RT.renderOneLine(currentLine)
        currentLine += 1
    pygame.display.flip()

pygame.display.quit()
