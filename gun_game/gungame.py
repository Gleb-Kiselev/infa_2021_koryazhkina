from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

GRAVITY_ACCELERATION = 1000 #px/s^2


class Ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0 #px/s
        self.vy = 0 #px/s
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30


        self.lastMoved = time.time()
        self.standingTime = 0

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        print(self.y, self.vy)
        now = time.time()
        timePassed = now - self.lastMoved


        if self.vx == 0 and self.vy == 0:
            self.standingTime += timePassed


        if self.standingTime >= 2:
            self.remove()
            return 'deleted'

        
        self.x = self.x + self.vx*timePassed
        self.y = self.y + self.vy*timePassed + GRAVITY_ACCELERATION*timePassed**2/2
        self.vy = self.vy + GRAVITY_ACCELERATION*timePassed


        windowWidth = 800
        windowHeight = 600
        walls = {'left': self.r, 'right': windowWidth - self.r, 'bottom': windowHeight - self.r}



        if self.x < walls['left']:
            self.x = walls['left']
            self.vx = -self.vx/2



        if self.x > walls['right']:
            self.x = walls['right']
            self.vx = -self.vx/2



        if self.y > walls['bottom']:
            self.y = walls['bottom']
            self.vy = -abs(self.vy/2)
            self.vx = self.vx/2


            if abs(self.vy) < 100:
                self.vy = 0
                self.vx = 0


        self.set_coords()
        self.lastMoved = now
        return 'saved'




        

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        dist = centerDistance(self, obj)
        if dist <= self.r + obj.r:
                return True

            
        else:
                return False



    def remove(self):
        canv.delete(self.id)




def centerDistance(circleObj1, circleObj2):


    x1, y1 = circleObj1.x, circleObj1.y
    x2, y2 = circleObj2.x, circleObj2.y


    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)







class Gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1


    def refreshAngle(self, cursorX, cursorY, baseX, baseY):
        if cursorX != baseX:
            self.an = math.atan((cursorY - baseY) / (cursorX - baseX))

        else:
            if cursorY > baseY:
                self.an = math.pi
            else:
                self.an = -math.pi


        

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        balls[new_ball.id] = new_ball
        new_ball.r += 5
        self.refreshAngle(event.x, event.y, new_ball.x, new_ball.y)
        new_ball.vx = self.f2_power * math.cos(self.an) * 10
        new_ball.vy = self.f2_power * math.sin(self.an) * 10
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.refreshAngle(event.x, event.y, 20, 450)
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target():
    
    # FIXME: doesn't work!!! How to call this functions when object is created?
    # self.id = canv.create_oval(0,0,0,0)
    # self.id_points = canv.create_text(30,30,text = self.points,font = '28')
    # self.new_target()

    def __init__(self):
        """ Инициализация новой цели. """
        self.live = 1
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        self.id = canv.create_oval(x-r, y-r, x+r, y+r, fill=color)

    

    def hit(self):
        """Попадание шарика в цель."""
        canv.delete(self.id)



class PointsText():
    def __init__(self):
        self.id = canv.create_text(30,30,text = '0',font = '28')
        self.points = 0


    def increase(self):
        self.points += 1
        canv.itemconfig(self.id, text=self.points)



screen1 = canv.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
balls = dict()
pointsText = PointsText()


def new_game(event=''):
    global g1, screen1, balls, bullet, pointsText
    t1 = Target()
    bullet = 0
    balls = dict()
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    def cycleDrawing():
        global balls
        
        newBalls = dict()

        
        for ballId in balls:
            b = balls[ballId]
            deletion = b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                pointsText.increase()
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')

            if deletion != 'deleted':
                newBalls[ballId] = b


        balls = newBalls
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()


    while t1.live or balls:
        cycleDrawing()



    canv.itemconfig(screen1, text='')
    root.after(750, new_game)


new_game()
tk.mainloop()
