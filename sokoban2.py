#! /usr/bin/env python26
# coding: utf-8
from pyroguelib.platform.media import MediaApp
from pyroguelib.model.main import MainApp
from pyroguelib.model.scene import *
from pyroguelib.model.tile import *
class TileUnit:
    def __init__(self,model,item):
        self.item = item
        self.layer = item.layer
        self.model = model
    def show(self):
        return u' '
    def push(self,dx,dy,obj):
        pass
    def __unicode__(self):
        return self.show()
class Box(TileUnit):
    def push(self,dx,dy,obj):
        if self.model.empty(*self.item.pos.by(dx,dy)):
            self.item.move(*self.item.pos.by(dx,dy))
    def show(self):
        return u'$'
class Player(TileUnit):
    def walk(self,dx,dy):
        np = self.item.pos.to(lambda x:x+complex(dx,dy))
        if self.layer.get(np,False):
            self.layer[np].push(dx,dy,self)
        if self.model.empty(*np):
            self.item.move(*np)
        self.model.view.see(self.item.pos,7,3)
    def show(self):
        return u'@'
class BoxWorld(TileModel):
    def empty(self,x,y):
        return self.unit.empty(x,y) and unicode(self.field.get((x,y),u' ')) in u'-.' 
    def isWin(self):
        return all(self.field.get(k,None)==u'.' for k,v in self.unit.items() if isinstance(v,Box))
    def __init__(self,data,tiles):
        self.unit = self.makeLayer()
        self.field = self.makeLayer()
        self.layers = [self.field,self.unit]
        self.view = self.makeView(self.layers,lambda x:unicode(x))
        self.view.size(16,6)
        TileBuild.fill(self.layers,data,tiles,lambda x,item:x(self,item) if not isinstance(x,unicode) else x )
        self.player = self.unit.find(lambda x:isinstance(x,Player))
        self.view.see(self.player.item.pos,7,3)
class BoxBuilder(TileBuild):
    levels = [
    u"""
__###___
__#.#___
__#-####
###$-$.#
#.-$@###
####$#__
___#.#__
___###__
""",
    u"""
####__
#-.#__
#--###
#*@--#
#--$-#
#--###
####__
""",
    
    ]
    tiles = {
    u'@' : [u'-',Player],
    u'+' : [u'.',Player],
    u'$' : [u'-',Box],
    u'*' : [u'.',Box],
    u'#' : [u'#'],
    u'.' : [u'.'],
    u'-' : [u'-'],
    u'_' : [u'_'],  
    True : [u'-']
    }
    model = BoxWorld
    def __init__(self):
        self.level = 0
        self.scene = None
    def build(self):
        return self.model(self.levels[self.level],self.tiles)
    def next(self):
        if self.hasNext():
            self.level += 1
    def hasNext(self):
        return self.level+1<len(self.levels)
class BoxScene(SceneItem):
    def __init__(self):
        SceneItem.__init__(self)
        self.levels = BoxBuilder()
        self.model = self.levels.build()
        self.show = None
    def onShow(self):
        return self.model.view() if not self.show else self.show
    def onDpad(self,dx,dy):
        self.model.player.walk(dx,dy)
        if self.model.isWin():
            if self.levels.hasNext():
                self.levels.next()
                self.model = self.levels.build()
            else:
                self.show = u'U Win!'
@MediaApp
class Hello(MainApp):
    def __init__(self,app):
        MainApp.__init__(self,app,BoxScene())
