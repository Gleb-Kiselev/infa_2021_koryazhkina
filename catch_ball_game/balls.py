from tkinter import *
from random import randrange as rnd, choice
import math
import time


FPS = 25
root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')


canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']


balls = {}

ballsLimit = 100

window = {}

timeForNewBall = time.time()


ballsIterator = 0
def newBall():
    '''Function creates a ball'''
    global timeForNewBall, ballsIterator
    if len(balls) < ballsLimit:
        balls['ballsIterator'] = {
            'x': rnd(100, 700),
            'y': rnd(100, 500),
            'r': rnd(30, 50),
            'velocity': [rnd(-50, 50), rnd(-50, 50)], #coordinates of velocity's vector (pixels per second)
            'lastMoved': time.time(),
            'livesUntil': time.time() + rnd(1000, 5000)/1000
        }


    ballsIterator += 1
    timeForNewBall = time.time() + rnd(500, 1500)/1000




def moveBall(ball):
    '''Moves the ball. (Removes it if it's life time is over.) Argument is an element from the balls' set'''
    now = time.time()
    if now >= ball['livesUntil']:
        balls.remove(ball)
        return


    timeFromLastMoving = now - ball['lastMoved']
    ball['x'] += ball['velocity'][0]*timeFromLastMoving
    ball['y'] += ball['velocity'][1]*timeFromLastMoving


    wallsForCenter = {
        'right': 800-ball['r'],
        'left': ball['r'],
        'top': ball['r'],
        'bottom': 600-ball['r']
    }

    

    if ball['x'] > wallsForCenter['right']:
        indent = ball['x']-wallsForCenter['right']
        ball['x'] = wallsForCenter['right']-indent
        ball['velocity'][0] *= -1

        

    if ball['x'] < wallsForCenter['left']:
        indent = wallsForCenter['left']-ball['x']
        ball['x'] = wallsForCenter['left']+indent
        ball['velocity'][0] *= -1


    if ball['y'] > wallsForCenter['bottom']:
        indent = wallsForCenter['bottom']-ball['y']
        ball['y'] = wallsForCenter['bottom']+indent
        ball['velocity'][1] *= -1

    if ball['y'] < wallsForCenter['top']:
        indent = wallsForCenter['top']-ball['y']
        ball['y'] = wallsForCenter['top']+indent
        ball['velocity'][1] *= -1


    ball['lastMoved'] = now




def drawBall(ball):
    '''Draws the ball on canvas. Argument is an element from the balls' set'''
    canv.create_oval(ball['x'] - ball['r'], ball['y'] - ball['r'], ball['x'] + ball['r'], ball['y'] + ball['r'], fill=choice(colors), width=0)


def distance(dot1, dot2):
    '''Returns the distance beetween dot1 and dot2.
    Arguments are pairs (x,y) with coordinates'''

    return math.sqrt( (dot2[0]-dot1[0])**2 + (dot2[1] - dot1[1])**2 )




def main():
    canv.delete(ALL)

    
    now = time.time()
    if now >= timeForNewBall:
        newBall()


    for ball in balls:
        moveBall(ball)
        drawBall(ball)



    root.after(1000/FPS, main)



def click(event):
    '''Event listener for click'''

    #if distance((event.x, event.y), (x, y)) <= r:
        
    
main()
canv.bind('<Button-1>', click)
root.mainloop()
