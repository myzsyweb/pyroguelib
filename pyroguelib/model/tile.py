#! /usr/bin/env python26
# coding: utf-8 
__all__ = ['TileItem','TileModel','TileBuild']
class TileShow:
    def __init__(self,getLayers=None,getTile=None):
        self.width,self.height = 0,0
        self.offsetX,self.offsetY = 0,0            
        self._getLayers = getLayers or (lambda:[])
        self._getTile = getTile or unicode
        self._blank = (lambda x,y:u' ')
        self._mask = (lambda x,y,wchar:wchar[0])
    def size(self,width,height):
        self.width,self.height = width,height
    def offset(self,x,y):
        self.offsetX,self.offsetY = x,y
    def see(self,point,x,y):
        self.offset(*point.by(-x,-y))
    def show(self):
        assert self.width!=0 and self.height != 0
        return (u'\n'.join( u''.join(self._mask(x,y,(
            lambda point:(lambda tile:self._getTile(tile) if tile else self._blank(*point))
            (reduce(lambda s,i:s if s else i.get(point,None) ,reversed(self._getLayers()),None)))
            ((x+self.offsetX,y+self.offsetY))) for x in range(self.width)) for y in range(self.height)) + u'\n')
    def __unicode__(self):
        return self.show()
    def __call__(self):
        return self.show()
class TileLayer(dict):
    @classmethod
    def fromList(cls,lst,key):
        return cls([key(i),i] for i in lst)
    @staticmethod
    def isTile(obj):
        return True
        return isinstance(obj,unicode) or hasattr(obj,'__unicode__') or len(unicode(obj)) == 1
    def __setitem__(self,k,v):
        assert isinstance(k,tuple) and self.isTile(v) and k not in self,"%s %s"%(k,v)
        return dict.__setitem__(self,k,v)
    def move(layer,oKey,nKey):
        layer[nKey] = layer.pop(oKey)
    def put(self,x,y,obj):
        self[(x,y)] = obj
    def at(self,x,y,default=None):
        return self.get((x,y),default)
    def empty(self,x,y):
        return (x,y) not in self
    def items(self):
        return dict.items(self)
    def tiles(self,pred=None):
        return [i for i in self.values() if pred(i)] if pred else self.values()
    def find(self,pred):
        tiles = self.tiles(pred)
        assert len(tiles)==1,len(tiles)
        return tiles[0]
class TilePoint(tuple):
    def __init__(self,obj):
        tuple.__init__(self,obj)
    @classmethod
    def at(cls,x,y):
        return cls([x,y])
    @classmethod
    def of(cls,pair):
        return cls(pair)
    def by(self,dx,dy):
        return self.at(*map(sum,zip(self,(dx,dy))))
    def to(self,transform):
        return (lambda x:self.at(x.real,x.imag))(transform(complex(*self)))
    def __complex__(self):#cp
        return complex(*self)
    def dt(self):
        return self.of(i/abs(i) if i else 0 for i in self)
class TileItem:
    def __init__(self,layer,x,y):
        self.pos = TilePoint.at(x,y)
        self.layer = layer
    def move(self,x,y):
        pos = TilePoint.at(x,y)
        self.layer.move(self.pos,pos)
        self.pos = pos
    def remove(self):
        self.layer.pop(self.pos)
class TileModel:
    @staticmethod
    def makeView(layers,tileOf=unicode):
        return TileShow(lambda:layers,tileOf)
    @staticmethod
    def makeLayer():
        return TileLayer()
class TileUnit:
    def __init__(self,item):
        self.item = item
class TileBuild:
    @classmethod
    def templ(cls,data,cell):
        bs = data.strip().split(u'\n')
        for y,line in enumerate(bs):
            for x,wchar in enumerate(line):
                cell(x,y,wchar)
    @classmethod
    def fill(cls,layers,data,tilemap,build=lambda x,item:x(item)):
        def builder(wchar):
            return tilemap[wchar] if wchar in tilemap else tilemap.get(True,None)
        def cell(x,y,wchar):
            makeTile = lambda item,layer:build(item,TileItem(layer,x,y))
            for layer,item in zip(layers,builder(wchar)):
                if item:
                    layer.put(x,y,makeTile(item,layer))
        return cls.templ(data,cell)
