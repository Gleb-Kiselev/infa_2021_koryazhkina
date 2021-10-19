import pygame
from pygame.draw import *
import math
pygame.init()

templateWidth = 2501
templateHeight = 1667
screenWidth = 1280
screenHeight = round(screenWidth/templateWidth * templateHeight)
pandTemplateWidth = 780
pandTemplateHeight = 873
FPS = 30
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()


def main():
    
    backgroundColor = (255, 175, 128)
    fillBackground(backgroundColor)
    
    drawTree({'x': 634/templateWidth*screenWidth,
              'y': 348/templateHeight*screenHeight,
              'width': 448/templateWidth*screenWidth,
              'height': 836/templateHeight*screenHeight,
              'color': (0, 104, 55),
              'timeLabel': pygame.time.get_ticks()})
    
    drawTree({'x': 585/templateWidth*screenWidth,
              'y': 0,
              'width': 1350/templateWidth*screenWidth,
              'height': 1134/templateHeight*screenHeight,
              'color': (0, 104, 55),
              'timeLabel': pygame.time.get_ticks()})



    drawTree({'x': 45/templateWidth*screenWidth,
              'y': 443/templateHeight*screenHeight,
              'width': 578/templateWidth*screenWidth,
              'height': 715/templateHeight*screenHeight,
              'color': (0, 104, 55),
              'timeLabel': pygame.time.get_ticks()})



    drawTree({'x': 1900/templateWidth*screenWidth,
              'y': 38/templateHeight*screenHeight,
              'width': 608/templateWidth*screenWidth,
              'height': 1054/templateHeight*screenHeight,
              'color': (0, 104, 55),
              'timeLabel': pygame.time.get_ticks()})


    now = pygame.time.get_ticks()
    



    smallPandInitialParams = {'x': 1024/templateWidth * screenWidth,
                              'y': 1185/templateHeight * screenHeight - 200,
                              'width': 383/templateWidth * screenWidth,
                              'height': 389/templateHeight * screenHeight}


    smallPandFinParams = {'x': 1024/templateWidth * screenWidth - 700,
                          'y': 1185/templateHeight * screenHeight - 300,
                          'width': 383/templateWidth * screenWidth * 2,
                          'height': 389/templateHeight * screenHeight * 2}



    smallPandParams = {}
    for key in smallPandInitialParams:
        paramValue1 = smallPandInitialParams[key]
        paramValue2 = smallPandFinParams[key]
        currentValue = walkInInterval(paramValue1, paramValue2, 3000, now)
        smallPandParams[key] = currentValue


    if math.floor(now/3000) % 2 == 0:
        smallPandParams['mirror'] = False
    else:
        smallPandParams['mirror'] = True


    smallPandParams['rotateAngle'] = walkInInterval(-20, 20, 500, now)
    smallPandParams['timeLabel'] = now



    drawPand(smallPandParams)




    drawPand({'x': 1329/templateWidth * screenWidth,
          'y': 600/templateHeight * screenHeight,
          'width': pandTemplateWidth/templateWidth * screenWidth,
          'height': pandTemplateHeight/templateHeight * screenHeight,
          'rotateAngle': 0,
          'mirror': False,
          'timeLabel': now})



    pygame.display.update()


    
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


    branches1 = [[(38/62, 13/65), (16/62, 3/65), (1/62, 5/65)],
                [(37/62, 24/65), (54/62, 16/65), (67/62, 14/65)],
                [(7/62, 23/65), (16/62, 21/65), (32/62, 27/65)],
                [(34/62, 44/65), (42/62, 36/65), (58/62, 34/65)]]


    branches2 = [[(30/62, 17/65), (16/62, 12/65), (2/62, 16/65)],
                [(33/62, 25/65), (43/62, 12/65), (58/62, 6/65)],
                [(7/62, 35/65), (18/62, 30/65), (30/62, 31/65)],
                [(34/62, 44/65), (41/62, 34/65), (50/62, 30/65)]]



    branches = []
    for i in range(4):
        curBranch = []
        branch1 = branches1[i]
        branch2 = branches2[i]

        for j in range(3):
            startDot = branch1[j]
            finDot = branch2[j]

            curDot = cycleTraectory(startDot, finDot, 1000, treeParams['timeLabel'])
            curBranch.append(curDot)


        branches.append(curBranch)


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


    segments1 = [ #every trunk's segment is the list of ranges [(x1, y1), (x2, y2), (x3, y3)...] with its vertexs' relative coordinates
        
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



    segment3Width = distance(segments1[2][2], segments1[2][3])
    segment3Height = distance(segments1[2][1], segments1[2][2])
    
    segment3Rotated = [(segments1[1][0][0], segments1[1][0][1] - 1/65 - segment3Height),
                       (segments1[1][0][0] + segment3Width, segments1[1][0][1] - 1/65 - segment3Height),
                       (segments1[1][0][0] + segment3Width, segments1[1][0][1] - 1/65),
                       (segments1[1][0][0], segments1[1][0][1] - 1/65)]



    segment4Width = distance(segments1[3][2], segments1[3][3])
    segment4Height = distance(segments1[3][1], segments1[3][2])
    
    segment4Rotated = [(segment3Rotated[0][0], segment3Rotated[0][1] - 1/65 - segment4Height),
                       (segment3Rotated[0][0] + segment4Width, segment3Rotated[0][1] - 1/65 - segment4Height),
                       (segment3Rotated[0][0] + segment4Width, segment3Rotated[0][1] - 1/65),
                       (segment3Rotated[0][0], segment3Rotated[0][1] - 1/65)]    



    segments2 = [segments1[0], segments1[1], segment3Rotated, segment4Rotated]


    segments = []
    for i in range(4):
        currentSegment = []
        startDots = segments1[i]
        finishDots = segments2[i]


        for j in range(4):
            curStartDot = startDots[j]
            curFinishDot = finishDots[j]
            curPosition = cycleTraectory(curStartDot, curFinishDot, 1000, treeParams['timeLabel'])
            currentSegment.append(curPosition)


        segments.append(currentSegment)


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


    startAngle = 10
    finAngle = startAngle*(coef+1)
    angle = walkInInterval(startAngle, finAngle, 1000, treeParams['timeLabel'])


    leafBox = pygame.Surface((absWidth, absLength), pygame.SRCALPHA)
    ellipse(leafBox, treeParams['color'], pygame.Rect(0, 0, absWidth, absLength))
    leafBox = pygame.transform.rotate(leafBox, coef*angle)
    boxWidth, boxHeight = leafBox.get_size()
    
    screen.blit(leafBox, (vertex[0] - boxWidth/2, vertex[1]))

    


    
def drawPand(pandParams):
    '''Draws the pand using the box model: the pand is bounded by box.
    pandParams - dictionary with box parametres {'x': x, 'y': y, 'width': width, 'height': height}'''



    surface = pygame.Surface((pandTemplateWidth, pandTemplateHeight), pygame.SRCALPHA)



    rightPawVertexes = [(153, 360), (200, 650), (160, 689), (97, 651), (109, 395), (153, 360)]
    leftForePawVertexes = [(473, 188), (454, 501), (404, 713), (326, 789), (247, 762), (473, 188)]
    backPawVertexes = [(687, 393), (558, 720), (479, 667), (687, 393)]
    faceVertexes = [(255, 136), (329, 174), (336, 365), (170, 398), (160, 198), (205, 136), (225, 136)]




    ellipse(surface, (255, 255, 255), (105, 145, 641, 364))
    roundedCornersPolygon(surface, (0,0,0), rightPawVertexes, 50)
    roundedCornersPolygon(surface, (0,0,0), leftForePawVertexes, 50)
    roundedCornersPolygon(surface, (0,0,0), backPawVertexes, 70)
    roundedCornersPolygon(surface, (255, 255, 255), faceVertexes, 100)




    if math.floor(pandParams['timeLabel']/200) % 6 == 0:
        #eyes drawing {
        leftEyeStartRect = (62, 264, 87, 131)
        leftEyeFinRect = (62, 264 + 131/2, 87, 0)
        leftEyeRect = []
        for i in range(4):
            currentValue = walkInInterval(leftEyeStartRect[i], leftEyeFinRect[i], 200, pandParams['timeLabel'])
            leftEyeRect.append(currentValue)
        
        ellipse(surface, (0,0,0), leftEyeRect)





        rightEyeStartRect = (262-64, 362-64, 64*2, 64*2)
        rightEyeFinRect = (262-64, 362, 64*2, 0)
        rightEyeRect = []
        for i in range(4):
            currentValue = walkInInterval(rightEyeStartRect[i], rightEyeFinRect[i], 200, pandParams['timeLabel'])
            rightEyeRect.append(currentValue)
        ellipse(surface, (0,0,0), rightEyeRect)


        #}

    else:
        ellipse(surface, (0,0,0), (62, 264, 87, 131))
        ellipse(surface, (0,0,0), (262-64, 362-64, 64*2, 64*2))


    
    ellipse(surface, (0,0,0), (81, 440, 103, 69))


    earLength = distance((189, 15), (26, 180)) - 50
    earWidth = distance((56, 51), (133, 127))


    earBox = pygame.Surface((earWidth, earLength), pygame.SRCALPHA)
    ellipse(earBox, (0,0,0), (0,0,earWidth, earLength))
    
    leftEarStartAngle = -40
    leftEarStopAngle = -70
    leftEarAngle = walkInInterval(leftEarStartAngle, leftEarStopAngle, 1000, pandParams['timeLabel'])         
    leftEar = pygame.transform.rotate(earBox, leftEarAngle)


    rightEarStartAngle = 20
    rightEarStopAngle = 60
    rightEarAngle = walkInInterval(rightEarStartAngle, rightEarStopAngle, 1000, pandParams['timeLabel'])
    rightEar = pygame.transform.rotate(earBox, rightEarAngle)

    surface.blit(leftEar, (17, 2))
    surface.blit(rightEar, (327, 48))




    surface = pygame.transform.scale(surface, (round(pandParams['width']), round(pandParams['height'])))
    surface = pygame.transform.rotate(surface, pandParams['rotateAngle'])
    surface = pygame.transform.flip(surface, pandParams['mirror'], False)
    screen.blit(surface, (pandParams['x'], pandParams['y']))





def roundedCornersPolygon(surface, color, vertexesList, cornerRadius):
    '''Draws the convex polygon with rounded corners.
    surface - pygame.Surface object for drawing
    color - color for drawing
    vertexesList - list [(x1, y1), (x2, y2)...] with coordinates of corner arcs' centers
    cornerRadius - radius for corners'''


    auxiliaryPolygonVertexes = []

    def rotateDirection(vector, nextVector):
        '''vector and nextVector are objects pygame.math.Vector2
        returns 1 if vector needs to be rotated counterclockwise and -1 else'''

        vectorPolarAngle = vector.as_polar()[1]
        nextVectorPolarAngle = nextVector.as_polar()[1]

        if nextVectorPolarAngle - vectorPolarAngle > 180:
            vectorPolarAngle += 360

        elif vectorPolarAngle - nextVectorPolarAngle > 180:
            nextVectorPolarAngle += 360



        if nextVectorPolarAngle > vectorPolarAngle:
            return -1

        else: return 1


    def translateSegment(vertex1, vertex2, translateVector):
        '''Moves the segment vertex1-vertex2 on translateVector
        vertex1, vertex2 - pairs (x, y) of coordinates
        translateVector - object pygame.math.Vector2
        Returns the list [A, B] with coordinates' pairs for new segment's vertexes'''

        newVertex1 = (vertex1[0] + translateVector[0], vertex1[1] - translateVector[1])
        newVertex2 = (vertex2[0] + translateVector[0], vertex2[1] - translateVector[1])

        return [newVertex1, newVertex2]
            
        
    for i in range(1, len(vertexesList)):
        auxiliaryPolygonVertexes.append(vertexesList[i-1])
        
        currentVector = [vertexesList[i], vertexesList[i-1]]
        nextVector = [vertexesList[i], vertexesList[ (i+1)%len(vertexesList) ] ]


        currentVectorX = currentVector[1][0] - currentVector[0][0]
        currentVectorY = -(currentVector[1][1] - currentVector[0][1])
        currentVectorObj = pygame.math.Vector2(currentVectorX, currentVectorY)
        currentVectorPolarAngle = currentVectorObj.as_polar()[1]


        nextVectorX = nextVector[1][0] - nextVector[0][0]
        nextVectorY = -(nextVector[1][1] - nextVector[0][1])
        nextVectorObj = pygame.math.Vector2(nextVectorX, nextVectorY)

        
        directionCoef = rotateDirection(currentVectorObj, nextVectorObj)

        normal = pygame.math.Vector2()
        normal.from_polar((cornerRadius, currentVectorPolarAngle + directionCoef*90))

        newSegment = translateSegment(vertexesList[i-1], vertexesList[i], normal)

        auxiliaryPolygonVertexes += newSegment
        auxiliaryPolygonVertexes.append(vertexesList[i])



    polygon(surface, color, auxiliaryPolygonVertexes)
    for vertex in vertexesList:
        circle(surface, color, vertex, cornerRadius)


        


def cycleTraectory(dot1, dot2, duration, now):
    '''This function moves the dot from dot1's position to dot2's position and back.
    Arguments:
    dot1 - pair (x1, y1) with coordinates of start position
    dot2 - pair (x2, y2) with coordinates of finish position
    duration - the duration of moving (ms)
    now - time elapsed since the start moment (ms)
    Returns dot's coordinates at the moment.'''

    x1,y1 = dot1
    x2,y2 = dot2
    movingVector = (x2 - x1, y2 - y1)


    fullMovings = math.floor(now/duration)
    restMoving = now - fullMovings*duration
    
    if fullMovings % 2 == 0:
        coef = restMoving/duration
        resVector = (coef*movingVector[0], coef*movingVector[1])
        return (x1+resVector[0], y1+resVector[1])
    else:
        coef = -restMoving/duration
        resVector = (coef*movingVector[0], coef*movingVector[1])
        return (x2+resVector[0], y2+resVector[1])




def walkInInterval(startValue, finValue, duration, now):
    '''This function smoothly changes a value from startValue to stopValue.
    Returns the value at the moment.
    Arguments:
    startValue - value at the initial time
    finValue - value at the end of moving
    duration - duration of moving from startValue to finValue (ms)
    now - time elapsed since the initial moment (ms)'''


    delta = finValue - startValue
    fullMovings = math.floor(now/duration)
    restMovingTime = now - fullMovings*duration

    if fullMovings % 2 == 0:
        coef = restMovingTime/duration
        return startValue + delta*coef
    else:
        coef = restMovingTime/duration
        return finValue - delta*coef


    
    



finished = False
while not finished:
    main()    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    clock.tick(FPS)

pygame.quit()
