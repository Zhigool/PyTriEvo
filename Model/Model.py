# -*- coding: utf-8 -*-
__author__ = 'Dmitry Sapronov'

import numpy as np
import thread
from time import sleep
from Population import *

class Model(object):
    
    def __init__(self):
        print("Model.__init__")
        self.STOPCALC = False
        self.count_click = 0
        self.view = 0
        self.dataOfImageSource = 0
        self.nameImageSource = ""
        self.imageSource = ""
        self.imageSave = ""
    
    def startCalc(self):
        print("startCalc")
        self.STOPCALC = False
        Population.bestMatch = 100000000
        thread.start_new_thread(self.run,())
        self.view.setGeneratBttnAsStop()
    def stopCalc(self):
        print("stopCalc")
        self.STOPCALC = True
        self.view.setGeneratBttnAsGenerate()


    def openFile(self):
        print("openFile")
        self.nameImageSource = self.view.openFile()

    def addView(self, view):
        print("addView")
        self.view = view

    def run(self):
        print("run")
        if self.nameImageSource != "":
            Population.setImageSource(self.nameImageSource)
            obj = Population()
            while self.STOPCALC == False:
                obj.reset()
                obj.paintPrimitive()
                obj.calcDifference()
                if obj.isBest():
                    self.view.updateImage(Population.imageBigResult.resize(Population.sourceSize, Image.ANTIALIAS))
                    print(Population.bestMatch)