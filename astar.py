# Implementation of the A* pathfinding algorithm
# Author: Michal Kubečka (241449)

import pygame
import csv
import sys
import re
from math import sqrt

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARK_RED = (128,0,0)
BLUE = (0,0,255)
DARK_BLUE = (0,0,128)
DARK_GREEN = (0, 128, 0)

# Variables
squareSize = 16
startX = 1
startY = 1
goalX = 1
goalY = 22
delay = 50
map = [ # default map 25x25
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1,-1,-1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1],
    [ 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1],
    [ 1, 1,-1, 1, 1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1,-1, 1, 1,-1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1,-1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1,-1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1],
    [ 1,-1, 1, 1, 1,-1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1,-1,-1,-1,-1,-1, 1, 1,-1,-1,-1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1],
    [-1, 1, 1,-1,-1, 1, 1, 1,-1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1],
    [-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-1,-1, 1, 1, 1, 1],
    [-1,-1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1],
    [ 1,-1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1],
    [ 1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Argument parse
for arg in sys.argv:
    if re.match('^--help$', arg):
        print("Usage: python3 ./astar.py [[arg1] [arg2] ...]")
        print("Arguments:")
        print("\t--help\t\t\tShow this help.")
        print("\t--squareSize=value\tSet square size.")
        print("\t--map=path/fileName.csv\tChoose file with a map to be solved.")
        print("\t--start=X,Y\t\tSet start coordinates as in matrix.")
        print("\t--goal=X,Y\t\tSet goal coordinates as in matrix.")
        print("\t--delay=time[ms]\tSet delay in milliseconds.")
        exit(0)
    elif re.match('^--squareSize=', arg):
        try:
            squareSize = int(re.sub('^--squareSize=', '',arg))
        except:
            sys.stderr.write('ERROR: Wrong argument syntax\n')
            exit(1)
    elif re.match('^--map=', arg):
        arg = re.sub('^--map=', '', arg)
        inputFile = open(arg, 'r')
        csvFile = csv.reader(inputFile, delimiter=',')
        map = []
        try:
            for row in csvFile:
                if row[-1] == '':
                    del row[-1]
                map.append([int(x) for x in row])   # Trying out List Comprehension
        except:
            sys.stderr.write("ERROR: Unexpected input file format\t")
            exit(1)
    elif re.match('^--start=', arg):
        try:
            arg = re.sub('^--start=', '', arg)
            startX = int(re.sub(',.*$', '', arg)) + 1
            startY = int(re.sub('^.*,', '', arg)) + 1
        except:
            sys.stderr.write('ERROR: Wrong argument syntax\n')
            exit(1)
    elif re.match('^--goal=', arg):
        try:
            arg = re.sub('^--goal=', '', arg)
            goalX = int(re.sub(',.*$', '', arg)) + 1
            goalY = int(re.sub('^.*,', '', arg)) + 1
        except:
            sys.stderr.write('ERROR: Wrong argument syntax\n')
            exit(1)
    elif re.match('^--delay=', arg):
        delay = int(re.sub('^--delay=', '', arg))
    elif arg == sys.argv[0]:
        pass
    else:
        sys.stderr.write('Wrong argument syntax. Program runs in default settings.\n')

# Class declarations
class Element:
    """Represents individual tile on the map."""
    def __init__(self, posX, posY, g, h, f, prevX, prevY):
        self.posX = posX
        self.posY = posY
        self.g = g          # Distance traveled
        self.h = h          # Heuristics
        self.f = f          # Fitness function = g + h
        self.prevX = prevX
        self.prevY = prevY

class Astar:
    """Represents the A* pathfinding algorithm."""
    def __init__(self, startX, startY, goalX, goalY):
        self.open = []          # The 'open' queue
        self.closed = []        # The 'closed' queue
        self.startX = startX
        self.startY = startY
        self.goalX = goalX
        self.goalY = goalY
        self.finished = False
        self.direction = 0
    def debugPrint(self):
        """Print contents of the 'open' and 'closed' queues."""
        print("Debug Print")
        print("Open:")
        for o in self.open:
            print(o.posX, o.posY, o.g, o.f, o.prevX, o.prevY)
        print("\nClosed:")
        for c in self.closed:
            print(c.posX, c.posY, c.g, c.f, c.prevX, c.prevY)
        print("####################")
    def appendOpen(self, el: Element):
        """Append a new element to the 'open' queue."""
        self.open.append(el)
    def appendClosed(self, el: Element):
        """Append a new element to the 'closed' queue."""
        self.closed.append(el)
    def findLowestOpen(self):
        """Find element with the lowest value of the 'f' attribute within the 'open' queue."""
        if len(self.open) == 0:
            return None
        minValue = self.open[0].f
        minIndex = 0
        for i in range(len(self.open)):
            if self.open[i].f < minValue:
                minValue = self.open[i].f
                minIndex = i
        return minIndex
    def popOpen(self):
        """Remove element from the 'open' queue with the lowest value of the 'f' attribute and move this element to the 'closed' queue."""
        index = self.findLowestOpen()
        self.appendClosed(self.open.pop(index))
        if (self.closed[-1].posX == self.goalX) and (self.closed[-1].posY == self.goalY):
            self.finished = True
    def addNewToOpen(self, X, Y):
        """Create a new element and append it to the 'open' queue."""
        g = self.closed[-1].g + map[Y][X]
        h = sqrt(((self.goalX - X) ** 2) + ((self.goalY - Y) ** 2))
        f = g + h
        for c in self.closed:
            if (c.posX == X) and (c.posY == Y):
                return
        for i in range(len(self.open)):
            el = self.open[i]
            if (el.posX == X) and (el.posY == Y):
                if g < el.g:
                    self.open[i].g = g
                    self.open[i].h = h
                    self.open[i].f = f
                    self.open[i].prevX = self.closed[-1].posX
                    self.open[i].prevY = self.closed[-1].posY
                return                    
        self.appendOpen(Element(X, Y, g, h, f, self.closed[-1].posX, self.closed[-1].posY))
    def expandElement(self):
        """Expand chosen element."""
        X = self.closed[-1].posX
        Y = self.closed[-1].posY
        if map[Y][X-1] >= 0:    # left
            self.addNewToOpen(X-1, Y)
        if map[Y][X+1] >= 0:    # right
            self.addNewToOpen(X+1, Y)
        if map[Y-1][X] >= 0:    # up
            self.addNewToOpen(X, Y-1)
        if map[Y+1][X] >= 0:    # down
            self.addNewToOpen(X, Y+1)
    def nextStep(self):
        """Perform next step according to the A* algorithm."""
        if len(self.open) == 0:
            return True
        self.popOpen()
        self.expandElement()
        return False
    def findPath(self):
        """If finish has been reached - return the final path."""
        if not self.finished:
            return None
        path = [(self.closed[-1].posX, self.closed[-1].posY)]
        X = self.closed[-1].prevX
        Y = self.closed[-1].prevY
        for i in range(len(self.closed)-1, 0, -1):
            # Searching for previous coordinates (going backwards)
            if (self.closed[i].posX == X) and (self.closed[i].posY == Y):
                path.append((self.closed[i].posX, self.closed[i].posY))
                X = self.closed[i].prevX
                Y = self.closed[i].prevY
        path.append((self.startX, self.startY))
        return reversed(path)

# Map processing
def addMapFrame(map):
    """Build a wall around the map."""
    for row in map:
        row.insert(0, -1)
        row.append(-1)
    width = len(map[0])
    row = []
    for i in range(width):
        row.append(-1)
    map.insert(0, row)
    map.append(row)
    return map

map = addMapFrame(map)

astar = Astar(startX, startY, goalX, goalY)
astar.appendOpen(Element(startX,startY,0,0,0,None,None))       # start

pygame.init()
gridSizeY = len(map)
gridSizeX = len(map[0])
# Check if the coordinates of start and goal are within the map and not on any wall.
if ((startX > gridSizeX - 2) or (startY > gridSizeY - 2) or
    (goalX > gridSizeX - 2) or (goalY > gridSizeY - 2) or
    (map[startY][startX] < 0) or (map[goalY][goalX] < 0)):
    sys.stderr.write("ERROR: Invalid start or goal coordinates.\n")
    pygame.quit()
    exit(1)

window = pygame.display.set_mode((gridSizeX * squareSize, gridSizeY * squareSize))
pygame.display.set_caption("Astar")

# Visualization functions
def drawGrid():
    """Draw grid."""
    for i in range(1, gridSizeY):
        pygame.draw.line(window, BLACK, (0, i * squareSize), (gridSizeX * squareSize, i * squareSize))
    for i in range(1, gridSizeX):
        pygame.draw.line(window, BLACK, (i * squareSize, 0), (i * squareSize, gridSizeY * squareSize))

def drawSquare(posX, posY, color):
    """Draw a square."""
    pygame.draw.rect(window, color, (posX * squareSize, posY * squareSize, squareSize, squareSize))

def drawMap():
    """Draw the map."""
    for y in range(0, gridSizeY):
        for x in range(0, gridSizeX):
            if map[y][x] == -1:
                drawSquare(x, y, DARK_RED)

def drawOpen():
    """Draw elements from the 'open' queue."""
    open = astar.open
    for element in open:
        drawSquare(element.posX, element.posY, BLUE)

def drawClosed():
    """Draw elements from the 'closed' queue."""
    closed = astar.closed
    for element in closed:
        drawSquare(element.posX, element.posY, DARK_BLUE)

def drawGoal():
    """Draw an 'X' where the goal is."""
    X = astar.goalX * squareSize
    Y = astar.goalY * squareSize
    width = squareSize * 3 // 16
    for i in range(round(width/2)):
        # All this just so that the 'X' does not extend outward the square it belongs to (which happens if I set the width to > 1)
        pygame.draw.line(window, RED, (X + i, Y), (X + squareSize, Y + squareSize - i), 1)
        pygame.draw.line(window, RED, (X, Y + i), (X + squareSize - i, Y + squareSize), 1)
        pygame.draw.line(window, RED, (X + squareSize - i, Y), (X, Y + squareSize - i), 1)
        pygame.draw.line(window, RED, (X + squareSize, Y + i), (X + i, Y + squareSize), 1)

def drawPath(path):
    """Draw the final path."""
    for p in path:
        drawSquare(p[0], p[1], DARK_GREEN)

# MAIN
running = True
while running:
    if astar.finished:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(WHITE)
    drawMap()
    drawOpen()
    drawClosed()
    drawGoal()
    drawGrid()
    pygame.display.update()
    if astar.nextStep():
        break
    pygame.time.delay(delay)

if not astar.finished:  # Goal has not been reached
    pygame.quit()
    exit(0)

path = astar.findPath()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(WHITE)
    drawMap()
    drawOpen()
    drawClosed()
    drawPath(astar.findPath())
    drawGoal()
    drawGrid()
    pygame.display.update()

pygame.quit()
