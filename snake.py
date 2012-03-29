#! /usr/bin/env python26
# coding: utf-8 
from pyroguelib.platform.media import MediaApp
import random
@MediaApp
class Snake:
    class Logic:
        def __init__(self):
            self.w,self.h = 16,6
            self.gold = (0,0)
            self.snake = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
            self.dh,self.dv = 1,0
            self.work = True
        def head(self,dh,dv):
            self.dh,self.dv = dh,dv
        def step(self):
            new = (self.snake[0][0]+self.dh,self.snake[0][1]+self.dv)
            if new in self.snake or not (0<=new[0]<16 and 0<=new[1]<6):
                #print 'Ouch!'
                self.work = False
            if new == self.gold:
                self.snake.append(None)
                self.gold = random.choice([(i,j) for i in range(16) for j in range(6) if (i,j) not in self.snake])
            self.snake = [new]+self.snake[:-1]
            #print self.snake
        def show(self):
            buf = []
            for y in range(8):
                for x in range(16):
                    if (x,y) in self.snake:
                        buf.append(u'@')
                    elif (x,y)==self.gold:
                        buf.append(u'$')
                    else:
                        buf.append(u' ')
            return u''.join(buf)
    def __init__(self,app):
        self.app = app
        self.logic = self.Logic()
        self.delay = 0
    def onPressed(self,button):
        if self.logic.work:
            self.logic.head(
             int(button=='R')-int(button=='L'),
             int(button=='D')-int(button=='U'))
    def onUpdate(self,delta):
        if self.logic.work:
            if self.delay > 500:
                self.delay -= 500
                self.logic.step()
            self.delay += delta
    def onPaint(self,app):
        if self.logic.work:
            app.puts(self.logic.show())
        else:
            app.puts(u'fail...')
