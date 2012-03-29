#! /usr/bin/env python26
# coding: utf-8 
from pyroguelib.platform.media import MediaApp
class BoxTile:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.ground = {}
        self.object = {}
        self.offsetX = 0
        self.offsetY = 0
        self.player = None
    def moveObject(self,oldPoint,newPoint):
        assert newPoint not in self.object
        self.object[newPoint] = self.object[oldPoint]
        del self.object[oldPoint]
    def setObject(self,x,y,obj):
        assert isinstance(obj,unicode) or hasattr(obj,'__unicode__')
        self.object[(x,y)] = obj
    def setGround(self,x,y,wchar):
        assert isinstance(wchar,unicode) or hasattr(wchar,'__unicode__')
        self.ground[(x,y)] = wchar
    def moveView(self,x,y):
        self.offsetX = x
        self.offsetY = y
    def isEmpty(self,x,y):
        return (x,y) not in self.object and self.ground.get((x,y),u' ') in u'-. '
    def isWin(self):
        return all(self.ground.get(k,None)==u'.' for k,v in self.object.items() if isinstance(v,Box))
    def show(self):
        return (u'\n'.join( u''.join((lambda point:unicode(self.object.get(point,self.ground.get(point,u' '))))((x+self.offsetX,y+self.offsetY)) for x in range(self.w)) for y in range(self.h)) + u'\n')
    def __unicode__(self):
        return self.show()
class BoxTileBuilder:
    def __init__(self,tile):
        self.tile=tile
    def build(self):
        bs = self.mapdata().strip().split(u'\n')
        for y,line in enumerate(bs):
            for x,wchar in enumerate(line):
                self.buildCell(x,y,wchar)
    def mapdata(self):
        return (
u"""
####__
#-.#__
#--###
#*@--#
#--$-#
#--###
####__
""")
    def buildCell(self,x,y,wchar):
        if wchar==u'@':
            self.tile.player = Player(self.tile,x,y)
            self.tile.setObject(x,y,self.tile.player)
            self.tile.setGround(x,y,u'-')
        elif wchar==u'+':
            self.tile.player = Player(self.tile,x,y)
            self.tile.setObject(x,y,self.tile.player)
            self.tile.setGround(x,y,u'.')
        elif wchar==u'$':
            self.tile.setObject(x,y,Box(self.tile,x,y))
            self.tile.setGround(x,y,u'-')
        elif wchar==u'*':
            self.tile.setObject(x,y,Box(self.tile,x,y))
            self.tile.setGround(x,y,u'.')
        elif wchar==u'#':
            self.tile.setGround(x,y,u'#')
        elif wchar==u'.':
            self.tile.setGround(x,y,u'.')
        elif wchar==u'-':
            self.tile.setGround(x,y,u'-')
        elif wchar==u'_':
            self.tile.setGround(x,y,u'_')
        else:
            self.tile.setGround(x,y,u'-')
class Box:
    def __init__(self,tile,x,y):
        self.tile=tile
        self.x=x
        self.y=y
    def push(self,dx,dy):
        if self.tile.isEmpty(self.x+dx,self.y+dy):
            self.tile.moveObject((self.x,self.y),(self.x+dx,self.y+dy))
            self.x+=dx
            self.y+=dy
    def __unicode__(self):
        return u'$'
class Player:
    def __init__(self,tile,x,y):
        self.x=x
        self.y=y
        self.tile=tile
    def put(self,x,y):
        self.x = x
        self.y = y
    def dmove(self,dx,dy):
        np = (self.x+dx,self.y+dy)
        if isinstance(self.tile.object.get(np,False),Box):
            self.tile.object[np].push(dx,dy)
        if self.tile.isEmpty(*np):
            self.tile.moveObject((self.x,self.y),(self.x+dx,self.y+dy))
            self.put(self.x+dx,self.y+dy)
    def __unicode__(self):
        return u'@'


@MediaApp
class TileGame:
    class Logic:
        def __init__(self):
            self.tile = BoxTile(16,6)
            self.model = BoxTileBuilder(self.tile)
            self.model.build()
    def __init__(self,app):
        self.app=app
        self.logic=self.Logic()
        self.playing=1
    def onPressed(self,button):
        print button
        if self.playing:
            self.logic.tile.player.dmove(
                 int(button=='R')-int(button=='L'),
                 int(button=='D')-int(button=='U'))
            if self.logic.tile.isWin():
                self.playing=0
            
    def onPaint(self,app):
        if self.playing:
            app.puts(unicode(self.logic.tile))
        else:
            app.puts(u'U Win!')
