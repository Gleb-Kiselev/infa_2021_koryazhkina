from tkinter import *
from random import randrange as rnd, choice
from PIL import Image, ImageTk
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

score = 0
timeRemains = 10


bombImage = Image.open('bomb.png')

boomImage = Image.open('boom.png')
boomImage = boomImage.resize((100, 100), Image.ANTIALIAS)
boomTkImage = ImageTk.PhotoImage(boomImage)





ballsIterator = 0
def newBall():
    '''Function creates a ball'''
    global timeForNewBall, ballsIterator
    if len(balls) < ballsLimit:
        isBomb = False
        if rnd(1, 15) == 1:
            isBomb = True

        
        balls[ballsIterator] = {
            'x': rnd(100, 700),
            'y': rnd(100, 500),
            'r': rnd(30, 50),
            'velocity': [rnd(-500, 500), rnd(-500, 500)], #coordinates of velocity's vector (pixels per second)
            'lastMoved': time.time(),
            'livesUntil': time.time() + rnd(5000, 10000)/1000,
            'isBomb': isBomb
        }

        if not isBomb:
            balls[ballsIterator]['color'] = choice(colors)
        else:
            ball = balls[ballsIterator]
            bomb = bombImage.resize([ball['r']*2, ball['r']*2], Image.ANTIALIAS)
            bombTkImage = ImageTk.PhotoImage(bomb)
            balls[ballsIterator]['image'] = bombTkImage


    ballsIterator += 1
    timeForNewBall = time.time() + rnd(100, 1000)/1000


def moveBall(ballKey):
    '''Moves the ball. (Removes it if its life time is over.) Argument is a key for the balls' dict'''
    ball = balls[ballKey]
    now = time.time()
    if now >= ball['livesUntil']:
        del balls[ballKey]
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
        ball['y'] = wallsForCenter['bottom']-indent
        ball['velocity'][1] *= -1

    if ball['y'] < wallsForCenter['top']:
        indent = wallsForCenter['top']-ball['y']
        ball['y'] = wallsForCenter['top']+indent
        ball['velocity'][1] *= -1


    ball['lastMoved'] = now




def drawBall(ball):
    '''Draws the ball on canvas. Argument is an element from the balls' dict'''
    if not ball['isBomb']:
        canv.create_oval(ball['x'] - ball['r'], ball['y'] - ball['r'], ball['x'] + ball['r'], ball['y'] + ball['r'], fill=ball['color'], width=0)
    

    else:
        canv.create_image(ball['x'], ball['y'], image=ball['image'])





def distance(dot1, dot2):
    '''Returns the distance beetween dot1 and dot2.
    Arguments are pairs (x,y) with coordinates'''

    return math.sqrt( (dot2[0]-dot1[0])**2 + (dot2[1] - dot1[1])**2 )





def showScore():
    '''Shows the score on the screen'''
    canv.create_text(790, 10, text='Score: '+str(score), anchor=NE, font="Sans 20")



def showTime():
    '''Shows the time on the screen'''
    canv.create_text(10, 10, text='Time: '+str(int(timeRemains)), anchor=NW, font="Sans 20")


    

explosed = False


def main():
    global explosed, timeRemains
    now = time.time()

    
    canv.delete(ALL)


    showScore()
    
    
    if not('lastMainTime' in window):
        window['lastMainTime'] = now

    timeFromLastStart = now - window['lastMainTime']
    timeRemains = timeRemains - timeFromLastStart
    window['lastMainTime'] = now

    if timeRemains < 0:
        mainFinish()
        return


    if explosed:
        drawBoom(window['lastExplosion']['x'], window['lastExplosion']['y'])
        if now - window['lastExplosion']['time'] >= 1:
            explosed = False
        
        root.after(int(1000/FPS), main)
        return


        

    showTime()
    
    if now >= timeForNewBall:
        newBall()



    for ballKey in list(balls):
        drawBall(balls[ballKey])
        moveBall(ballKey)


    root.after(int(1000/FPS), main)



def click(event):
    '''Event listener for click'''
    global score, timeRemains
    for ballKey in list(balls):
        ball = balls[ballKey]
        x, y = ball['x'], ball['y']
        if distance((event.x, event.y), (x, y)) <= ball['r']:
            if not ball['isBomb']:
                score += 10
                timeRemains += 10
                del balls[ballKey]
            else:
                
                window['lastExplosion'] = {
                    'x': ball['x'],
                    'y': ball['y'],
                    'time': time.time()
                }
                
                drawBoom(ball['x'], ball['y'])
                return




def drawBoom(x, y):
    '''Effect of explosed bomb.'''
    global explosed, score, balls
    canv.delete(ALL)

    score = 0
    showScore()
    showTime()


    balls = {}

    canv.create_image(x, y, image=boomTkImage)
    
    explosed = True



def mainFinish():
    '''Draws the game's end screen'''
    canv.delete(ALL)
    window['nameInput'] = Entry(canv)
    window['button'] = Button(canv, text="Submit")


    canv.create_text(400, 70, text="Game over! You scored " + str(score), font="Sans 20")
    canv.create_text(400, 110, text="Enter your name: ", font="Sans 20")
    canv.create_window(400, 140, window=window['nameInput'], width=150, height=20)
    canv.create_window(400, 200, window=window['button'], width=100, height=20)
    window['button'].bind('<Button-1>', submit)
    canv.update()




def submit(event):
    name = window['nameInput'].get()
    if name.split() == []:
        canv.create_text(400, 250, text="Please enter the name.", font="Sans 10")
    else:
        canv.delete(ALL)
        canv.create_text(400, 300, text='Your result is written.', font="Sans 20")
        writeResult(name, score)


    canv.update()
        


def writeResult(name, score):
    file = open('results.log', 'a')
    file.write(name + ':    ' + str(score) + '\n')
    file.close()


    
    
main()
canv.bind('<Button-1>', click)
root.mainloop()
