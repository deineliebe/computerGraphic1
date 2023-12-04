import pygame
import numpy as np
import math

# Colors' initialization
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (230, 231, 232)

# There are parameters of our window (initialization)
WIDTH = 600
HEIGHT = 600
# Set title
pygame.display.set_caption("First lab (group: 0323, team: 4)")
# Set window's parameters
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Scale of object's vertices
scale = 100

# Set position of the object
position = [WIDTH / 2, HEIGHT / 2]

yAngle = 0
zAngle = -0.1;
xAngle = 0.6;

# Initialize cube vertices
points = []
points.append(np.matrix([0, 0, 1]))
points.append(np.matrix([1, 0, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([0, 1, 1]))
points.append(np.matrix([0, 0, 0]))
points.append(np.matrix([1, 0, 0]))
points.append(np.matrix([1, 1, 0]))
points.append(np.matrix([0, 1, 0]))

xShift = 1
yShift = 0
zShift = 0

for point in points:
    point += [xShift, yShift, zShift]

projectionMatrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projectedPoints = [
    [n, n] for n in range(len(points))
]


# Initialize coordinate vertices
coordinatePoints = []
coordinatePoints.append(np.matrix([[0], [0], [0]]))
coordinatePoints.append(np.matrix([[1], [0], [0]]))
coordinatePoints.append(np.matrix([[0], [-1], [0]]))
coordinatePoints.append(np.matrix([[-0.5], [0.5], [0]]))


projectedObjectPoints = [
    [n, n] for n in range(len(points))
]

projectedCoordinatesPoints = [
    [n, n] for n in range(len(coordinatePoints))
]

def connectPoints(i, j, points):
    pygame.draw.line(window, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

def createMatrix():
    for i in range(0, int(HEIGHT / 2), scale):
        pygame.draw.line(window, GREY, (0, i), (WIDTH, i))
    for i in range(int(HEIGHT / 2), HEIGHT, int(scale / 2)):
        pygame.draw.line(window, GREY, (0, i), (WIDTH, i))
    for j in range(0, WIDTH, scale):
        pygame.draw.line(window, GREY, (j, 0), (j, int (HEIGHT / 2)))
    for j in range(0, WIDTH * 2, scale):
        pygame.draw.line(window, GREY, (j, int (HEIGHT / 2)), (j - 3 * scale, HEIGHT))

def displayCube():
    i = 0
    # Display object's vertices & their rotation
    for point in points:
        rotated2D = np.dot(yRotation, point.reshape(3, 1))
        rotated2D = np.dot(xRotation, rotated2D)
        rotated2D = np.dot(zRotation, rotated2D)

        projected2D = np.dot(projectionMatrix, rotated2D)

        x = int(projected2D[0][0] * scale) + position[0]
        y = int(projected2D[1][0] * scale) + position[1]

        projectedPoints[i] = [x, y]
        pygame.draw.circle(window, RED, (x, y), 2)
        i += 1

    # Link cube's vertices
    for p in range(4):
        connectPoints(p, (p + 1) % 4, projectedPoints)
        connectPoints(p + 4, ((p + 1) % 4) + 4, projectedPoints)
        connectPoints(p, (p + 4), projectedPoints)

def displayCoordinates():
    # Display coordinate vertices
    for j in range(1, 8):
        for i in range(4):
            x = int(position[0] + j * scale * coordinatePoints[i][0])
            y = int(position[1] + j * scale * coordinatePoints[i][1])
            projectedCoordinatesPoints[i] = [x, y]
            pygame.draw.circle(window, RED, (x, y), 2)

    # Link coordinate vertices
    connectPoints(0, 1, projectedCoordinatesPoints)
    connectPoints(0, 2, projectedCoordinatesPoints)
    connectPoints(0, 3, projectedCoordinatesPoints)

clock = pygame.time.Clock()
while True:

    clock.tick(60)

    xRotation = np.matrix([
        [1, 0, 0],
        [0, math.cos(xAngle), -math.sin(xAngle)],
        [0, math.sin(xAngle), math.cos(xAngle)],
    ])

    yRotation = np.matrix([
        [math.cos(yAngle), 0, math.sin(yAngle)],
        [0, 1, 0],
        [-math.sin(yAngle), 0, math.cos(yAngle)],
    ])

    zRotation = np.matrix([
        [math.cos(zAngle), -math.sin(zAngle), 0],
        [math.sin(zAngle), math.cos(zAngle), 0],
        [0, 0, 1],
    ])

    yAngle += 0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Make window's color white
    window.fill(WHITE)
    createMatrix()
    displayCube()

    displayCoordinates()

    pygame.display.update()