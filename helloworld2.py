#! /usr/bin/env python26
# coding: utf-8
from pyroguelib.platform.media import MediaApp
from pyroguelib.model.main import MainApp
from pyroguelib.model.scene import *
@MediaApp
class Hello(MainApp):
    class MainScene(SceneItem):
        def onShow(self):
            return u'  Hello World'
