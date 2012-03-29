#! /usr/bin/env python26
# coding: utf-8
from scene import SceneItem,SceneBox
__all__ = ['MainApp']
class MainApp:
    class MainScene(SceneItem):
        def __init__(self):
            SceneItem.__init__(self)
        show = '  Hello World'
    def __init__(self,app,scene=None):
        self.app = app
        self._scene = SceneBox()
        self._scene.set(scene or self.MainScene())
        self._debug = True
    @property
    def scene(self):
        return self._scene     
    def setScene(self,scene):
        self._scene.set(scene)
    def onPressed(self,button):
        if self._debug:
            print button
        self._scene.onPress(button)
    def onUpdate(self,delta):
        self._scene.onUpdate(delta)
    def onPaint(self,app):
        self._scene.onPaint(app)
