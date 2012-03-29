#! /usr/bin/env python26
# coding: utf-8
__all__ = ['MediaApp']
import pygame
class MediaApp:
    import pygame
    singleton = None
    model = None
    caption = ""
    screenwidth = 640
    screenheight = 480
    bgcolor = (0,0,0)
    fgcolor = (255,255,255)
    framerate = 30
    fontsize = 80
    #save = {}
    #env = {}
    #cache = {}
    projection = 0
    keymap = {
        pygame.K_LEFT:  'L',
        pygame.K_RIGHT: 'R',
        pygame.K_UP:    'U',
        pygame.K_DOWN:  'D',
        pygame.K_z:     'A',
        pygame.K_x:     'B',
        pygame.K_c:     'S',
        }
    keyfullscreen = pygame.K_f
        #fullscreen change by 'F'
    """
    not use float,just use int
    """
    def __init__(self,modelFactory=lambda x:None):
        assert modelFactory is not None
        self.setModel(modelFactory(self))
        self.run()
    @classmethod
    def init(self):
        assert self.singleton is None
        self.singleton = self
        pygame.init()
        self.screen = pygame.display.set_mode([self.screenwidth,self.screenheight])
        pygame.display.set_caption('Media App')
        self.screen.fill([0,0,0])
        self.clock = pygame.time.Clock()
        self.lines = self.screenheight/self.fontsize
        self.columns = self.screenwidth*2/self.fontsize
        self.zhfont = pygame.font.SysFont("黑体", self.fontsize)
        self.enfont = pygame.font.SysFont("monospace", self.fontsize)
        assert self.zhfont.size("黑") and self.enfont.size("w") 
        self._line = 0
        self._column = 0
    @classmethod
    def setModel(self,model):
        self.model = model
    @classmethod
    def update(self):
        pygame.display.update()
    @classmethod
    def frame(self,delta):
        pygame.display.set_caption(self.caption+" "+"press Esc to quit. FPS: %.2f" % (self.clock.get_fps()))
        if self.model and hasattr(self.model,'frame'):
            return self.model.frame(delta)
        else:
            return self.dispatchFrame(delta)
    @classmethod
    def event(self,event):
        if self.model and hasattr(self.model,'event'):
            return self.model.event(event)
        else:
            return self.dispatchEvent(event)
    @classmethod
    def dispatchFrame(self,delta):
        if self.model and hasattr(self.model,'onUpdate'):
            self.model.onUpdate(delta)
        if self.model and hasattr(self.model,'onPaint'):
            self.clrscr()
            self.model.onPaint(self)
            self.paint()
    @classmethod
    def dispatchEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if self.model and hasattr(self.model,'onPressed'):
                if event.key in self.keymap:
                    self.model.onPressed(self.keymap.get(event.key))
    @classmethod
    def clrscr(self):
        self.screen.fill(self.bgcolor)
        self._line = 0
        self._column = 0
    @classmethod
    def puts(self,string):
        assert isinstance(string,unicode),(type(string),string)
        if self._line >= self.lines:
            return string
        if string:
            if string[0]=='\n':
                self._line  += 1
                self._column = 0
            else:
                font = (self.zhfont,self.enfont)[string[0]<u'\u1000']
                charwidth = int(font.size(string[0])[0]*2/self.fontsize)
                if (self._column+charwidth)*self.fontsize/2 > 640:
                    self._line  += 1
                    self._column = 0
                self.screen.blit(font.render(string[0], 0, self.fgcolor), 
                 (self._column*self.fontsize/2-0,self._line*self.fontsize-5))#!
                self._column += charwidth
            return self.puts(string[1:])
    @classmethod
    def write(self,obj):
        return self.puts(u''.join(obj))
    @classmethod
    def paint(self):
        pygame.display.update()
    @classmethod
    def loop(self):
        @apply
        def block():
            while True:
                tick_time = self.clock.tick(self.framerate)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return
                        #elif event.key == self.keyfullscreen:
                            #pygame.display.toggle_fullscreen()
                    self.event(event)
                self.frame(tick_time)
        self.singleton = None
    @classmethod
    def run(self):
        self.init()
        self.loop()
    @classmethod
    def time(self):
        return pygame.time.get_ticks()
if __name__=='__main__':
    @MediaApp
    class Dummy:
        def __init__(self,app):
            pass
