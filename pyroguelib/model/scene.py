#! /usr/bin/env python26
# coding: utf-8 
__all__ = ['SceneBox','SceneItem']
################# SceneBox ##################
class Scene:
    def onUpdate(self,delta):
        pass
    def onPress(self,button):
        pass
    def onPaint(self,graph):
        pass
    def onEnter(self):
        pass
    def onLeave(self):
        pass
class SceneBox(Scene):
    def __init__(self,scene=None):
        self._scene = scene or Scene()
        self._stack = []
    def set(self,scene):
        self._scene = scene
        self._scene.onEnter()
    def push(self):
        print "push scene",self._scene
        self._stack.append(self._scene)
    def pop(self):
        print "pop scene",self._stack[-1]
        self._stack[-1].onLeave()
        self.set(self._stack.pop())
    def call(self,scene):
        self.push()
        self.set(scene)
    def ret(self,value):
        self.pop()
        return value
    def onUpdate(self,delta):
        self._scene.onUpdate(delta)
    def onPress(self,button):
        self._scene.onPress(button)
    def onPaint(self,graph):
        self._scene.onPaint(graph)
    def onEnter(self):
        self._scene.onEnter()
    def onLeave(self):
        self._scene.onLeave()

################ SceneItem ##############
class Timer:
    class Delay:
        def __init__(self,timer,interval,action,init=0):
            self.timer = timer
            self.delay = init
            self.interval = interval
            self.action = action
        def __call__(self,delay):
            while self.delay > self.interval:
                self.delay -= self.interval
                if not self.action(self.delay):
                    self.timer.remove(self)
                    break
            self.delay += delay
    def __init__(self):
        self._box = []
        self.time = 0
    def __call__(self,delta):
        for timer in self._box:
            timer(delta)
        self.time += delta
    def remove(self,item):
        self._box.remove(item)
    def every(self,time,action):
        self.delay(time,lambda x:action() or True,0)
    def at(self,time,action):
        self.delay(self.time+time,lambda x:action() and False,0)
    def delay(self,time,action,init=0):
        self._box.append(self.Delay(self,time,action))
    def delayCall(self,time):
        return lambda x:self.delay(time,x)
    def everyCall(self,time):
        return lambda x:self.every(time,x)
    def delayYield(self,time):
        d = (lambda x:(lambda y:lambda z:not next(y,1))(iter(x())))
        return lambda x:self.delay(time,d(x))
class SceneItem(Scene):
    def __init__(self,show=None,dpad=None,menu=None,back=None,ok=None):
        #Scene.__init__(self)
        self._show = show
        self._draw = None
        self._dpad = dpad
        self._turn = None
        self._ok,self._back,self._menu = ok,back,menu 
        self.timer = Timer()
    def onPress(self,button):
        if button=='A':
            self.onOk()
        elif button=='B':
            self.onBack()
        elif button=='S':
            self.onMenu()
        else:
            self.onDpad(
                int(button=='R')-int(button=='L'),
                int(button=='D')-int(button=='U'))
    def onPaint(self,graph):
        self.onDraw(graph)
    def onUpdate(self,delta):
        self.timer(delta)
    def onDpad(self,dh,dv):
        if self._dpad:
            self._dpad(dh,dv)
    def onDraw(self,graph):
        graph.write(self.onShow())
    def onShow(self):
        if self._show:
            return self._show()
        else:
            return u''
    def onOk(self):
        if self._ok:
            self._ok()
    def onBack(self):
        if self._back:
            self._back()
    def onMenu(self):
        if self._menu:
            self._menu()

