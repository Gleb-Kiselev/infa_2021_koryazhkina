import pygame
from pygame.draw import *
import math
pygame.init()

screenWidth = 1280
screenHeight = 720
templateWidth = 2501
templateHeight = 1667
FPS = 30
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()


def main():
    backgroundColor = (255, 175, 128)
    fillBackground(backgroundColor)
    drawTree({'x': 585/templateWidth*screenWidth,
              'y': 0,
              'width': 1350/templateWidth*screenWidth,
              'height': 1134/templateHeight*screenHeight,
              'color': (0, 104, 55)})

def fillBackground(color):
    '''Fills the background with the received color.'''
    rect(screen, color, (0,0, screenWidth,screenHeight))




def drawTree(treeParams):
    '''Draws the tree using the box model: as tree has a box around it.
    treeParams is dictionary with parametres of tree's box. Structure:
    treeParams = {'x': x, 'y': y, 'width': width, 'height': height, 'color': color}
    x,y are coordinates of left-top box's corner, and width,height are sizes of the box.
    '''

    drawTrunk(treeParams)


    branches = [[(38/62, 13/65), (16/62, 3/65), (1/62, 5/65)],
                [(37/62, 24/65), (54/62, 16/65), (67/62, 14/65)],
                [(7/62, 23/65), (16/62, 21/65), (32/62, 27/65)],
                [(34/62, 44/65), (42/62, 36/65), (58/62, 34/65)]]


    listsForLeaves = [[3, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 2, 3],
                      [3, 2, 2, 1],
                      [1, 1, 1, 2]]


    leavesVertexesLists = []

    for i in range(len(branches)):
        vertexes = drawBranch(branches[i], treeParams, listsForLeaves[i])
        leavesVertexesLists.append(vertexes)


    for i in range(len(leavesVertexesLists)):
        currentBranchVertexes = leavesVertexesLists[i]

        if i % 2 == 0:
            tilt = 'left'
        else:
            tilt = 'right'

        for vertex in currentBranchVertexes:
            drawLeaf(vertex, 7/65, 2/62, tilt, treeParams)



def absolutizeX(x, boxParams):
    '''This function receives the X relative coordinate, measured in a box as a distance from the dot to the left side of box.
    Units - part of the full box's width.
    This function converts relative coordinate to absolute in pixels'''

    return x*boxParams['width'] + boxParams['x']


def absolutizeY(y, boxParams):
    '''Converts Y relative coordinate to absolute (see more in absolutizeX)'''

    return y*boxParams['height'] + boxParams['y']


def absolutizeList(coordsList, boxParams):
    '''This function receives the list of ranges with vertexs' relative coordinates and converts them to absolute:
    [(x1rel, y1rel), (x2rel, y2rel)...]    ->    [(x1abs, y1abs), (x2abs, y2abs)...]''' 
    res = []
    for coordsRange in coordsList:
        res.append(     ( absolutizeX(coordsRange[0], boxParams),     absolutizeY(coordsRange[1], boxParams) )    )
    
    return res







def drawTrunk(treeParams):
    '''Draws the trunk for the tree.
    treeParams - parametres of the tree's box (see drawTree)
    '''


    segments = [ #every trunk's segment is the list of ranges [(x1, y1), (x2, y2), (x3, y3)...] with its vertexs' relative coordinates
        
        [(30/62, 52/65),
         (34/62, 52/65),
         (34/62, 1),
         (30/62, 1)],


        [(30/62, 38/65),
         (34/62, 38/65),
         (34/62, 51/65),
         (30/62, 51/65)],


        [(34/62, 23/65),
         (37/62, 25/65),
         (34/62, 35/65),
         (31/62, 33/65)],


        [(40/62, 10/65),
         (41/62, 11/65),
         (36/62, 21/65),
         (35/62, 20/65)]


    ]




    for segment in segments:
        polygon(screen, treeParams['color'], absolutizeList(segment, treeParams))


def distance(dot1, dot2):
    '''Counts the distance beetween two dots, parametres are ranges (x, y) with their coordinates'''
    x1, y1 = dot1
    x2, y2 = dot2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def angleABCRads(A, B, C):
    '''Counts the angle ABC. Parametres are ranges (x, y) with coordinates of dots A, B and C. Result is in radians'''
    AC = distance(A, C)
    AB = distance(A, B)
    BC = distance(B, C)


    cosinus = (AB**2 + BC**2 - AC**2)/(2*AB*BC)
    return math.acos(cosinus)





def drawArc(dot1, dot2, dot3, color):
    '''Draws the arc by three dots.
    Each argument is the pair of coordinates.
    Returns the dictionary {'center': (x, y), 'radius': r, 'startAngle': startAngle, 'stopAngle': stopAngle}, where:
    center - range (x, y) with coordinates of arc's center
    radius - radius of arc
    startAngle - start dot's polar angle (in radians)
    stopAngle - stop dot's polar angle (in radians)'''
    dots = [dot1, dot2, dot3]
    x1, y1 = dot1
    x2, y2 = dot2
    x3, y3 = dot3

    xA = (x1+x2)/2
    yA = (y1+y2)/2

    xB = (x2+x3)/2
    yB = (y2+y3)/2

    coef3 = (x3 - x2)/(y3 - y2)
    coef2 = (x2 - x1)/(y2 - y1)

    centX = (yB - yA - coef2*xA + coef3*xB)/(coef3 - coef2)

    centY = yA - coef2*(centX - xA)
    center = (centX, centY)

    radius = distance(center, dot1)

    circumRect = pygame.Rect(centX - radius, centY - radius, radius*2, radius*2)

    auxiliaryDot = (centX + 1000, centY)


    def polarAngleRads(dot):
        '''Returns the polar angle of the dot (polar axis is center-auxiliaryDot).
        Argument is the pair of dot's coordinates.
        Result is in radians'''

        if dot[1] > centY:
            coef = -1
        else:
            coef = 1


        return coef*angleABCRads(dot, center, auxiliaryDot)
    

    
    angles = [polarAngleRads(dot1), polarAngleRads(dot2), polarAngleRads(dot3)]
    startAngle = min(angles)
    stopAngle = max(angles)
    arc(screen, color, circumRect, startAngle, stopAngle)


    return {'center': center, 'radius': radius, 'startAngle': startAngle, 'stopAngle': stopAngle}




def drawBranch(branch, treeParams, listForLeaves):
    '''Draws the  tree's branch.
    branch - list with pairs (x, y) of relative coordinates of three branches dots (beginning, middle, end)
    treeParams - object treeParams (see drawTree)
    listForLeaves - list [a1, a2, a3... an] with numbers.
        It's used for preparing leaves' vertexes: length of the arcs beetween neighbour vertexes will relate as a1:a2:a3...
        By the way, a1 is for the arc beetween the start branch's dot and the first leaf's dot.
        And so an is for the arc beetween the last leaf's dot and the last branch's dot.
        So minimal length of this list is 2: the list [a1, a2] means, that the branch has one leaf,
        and arc beetween the start branch's dot and the leaf relates to the arc beetween the leaf and the end branch's dot as a1:a2.
    Returns the list [(x1, y1), (x2, y2)...] with coordinates of vertexes for leaves'''
    branchAbs = absolutizeList(branch, treeParams)
    arcDict = drawArc(branchAbs[0], branchAbs[1], branchAbs[2], treeParams['color'])
    branchArcAngle = arcDict['stopAngle'] - arcDict['startAngle']

    def polarToDecart(center, radius, angleRads):
        '''Converts polar coordinates to decart
        center - coordinates of the polar center
        radius, angleRads - polar coordinates
        '''

        auxiliaryDot = (center[0] + 100, center[1])
        preX = math.cos(angleRads) * radius
        preY = math.sin(angleRads) * radius
        x = preX + center[0]
        y = center[1] - preY
        return (x, y)


    denominator = sum(listForLeaves)
    leavesPolarAngles = []
    runningAngle = arcDict['startAngle']
    for i in range( len(listForLeaves) - 1 ):
        runningAngle += listForLeaves[i]/denominator * branchArcAngle
        leavesPolarAngles.append(runningAngle)


    vertexesForLeaves = []
    for angle in leavesPolarAngles:
        vertexesForLeaves.append( polarToDecart(arcDict['center'], arcDict['radius'], angle) )


    return vertexesForLeaves
    


def drawLeaf(vertex, length, width, tilt, treeParams):
    '''This function draws the leaf.
    vertex - pair (x, y) with coordinates of leaf stalk's dot
    length, width - relative sizes of the leaf: relative length (width) is the absolute length (width) divided by tree box's height (width)
    tilt - string 'right' or 'left' - it determines, where the leaf will be tilted.
    treeParams - dictionary treeParams (see drawTree)'''

    absLength = length * treeParams['width']
    absWidth = width * treeParams['height']


    if tilt == 'right': coef = 1
    else: coef = -1


    leafBox = pygame.Surface((absWidth, absLength), pygame.SRCALPHA)
    ellipse(leafBox, treeParams['color'], pygame.Rect(0, 0, absWidth, absLength))
    leafBox = pygame.transform.rotate(leafBox, coef*10)
    boxWidth, boxHeight = leafBox.get_size()
    
    screen.blit(leafBox, (vertex[0] - boxWidth/2, vertex[1]))

    


    

    
    


main()

pygame.display.update()
finished = False
while not finished:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    clock.tick(FPS)

pygame.quit()
