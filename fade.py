#! /usr/bin/env python26
# coding: utf-8
from pyroguelib.platform.media import MediaApp
from pyroguelib.model.main import MainApp
from pyroguelib.model.scene import *
@MediaApp
class Hello(MainApp):
    class MainScene(SceneItem):
        def __init__(self):
            SceneItem.__init__(self)
            self.c = u' '
            @self.timer.delayYield(100)
            def _():
                for i in u"9876543210 ":
                    self.c = i*16*6
                    yield
        def onShow(self):
            return self.c
