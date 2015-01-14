# -*- coding: utf-8 -*-
import numpy as np
import random as rnd
import time
import sys

from PIL import Image, ImageDraw, ImageFilter,ImageEnhance

class Population(object):
    """docstring for Population"""
    sourceSize = ()
    resultQuality = 4
    imageSource = ""
    ndArraySource = ""
    imageBigResult = ""
    bestMatch = 100000000
    @staticmethod
    def setImageSource(str):
        Population.imageSource = Image.open(str).convert("RGB")
        Population.sourceSize = Population.imageSource.size[0], Population.imageSource.size[1]
        Population.ndArraySource = np.array(Population.imageSource.getdata()).reshape(Population.sourceSize[0], Population.sourceSize[1], 3)
        Population.imageBigResult = Image.new("RGBA", (Population.sourceSize[0]*Population.resultQuality, Population.sourceSize[1]*Population.resultQuality), (0,0,0,0))

    def __init__(self, numPrimitives=1):
        self.resultSize = Population.sourceSize[0], Population.sourceSize[1]
        self.resultType = Population.imageSource.mode
        self.numPrimitives = numPrimitives
        self.resultQuality = Population.resultQuality
        self.resultBigSize = self.resultSize[0]*self.resultQuality, self.resultSize[1]*self.resultQuality
        self.result = Population.imageBigResult.copy()

    def paintPrimitive(self):
        primitive= Image.new("RGBA", (self.resultBigSize[0], self.resultBigSize[1]), (0,0,0,0))
        drawPrimitive = ImageDraw.Draw(primitive)

        for cntTr in xrange(self.numPrimitives):
            x1, x2, x3 = rnd.sample(range(0, self.resultBigSize[0]), 3)
            y1, y2, y3 = rnd.sample(range(0, self.resultBigSize[1]), 3)
            color = tuple(rnd.sample(range(0, 255), 3))
            drawPrimitive.polygon((x1,y1,x2,y2,x3,y3), outline=color, fill=color)
            opacity = 0.5
            self.addTriangle(primitive, opacity)

    def addTriangle(self, primitive, opacity):
        if opacity < 1:
            alpha = primitive.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            primitive.putalpha(alpha)
        self.result = Image.alpha_composite(self.result, primitive)

    def calcDifference(self): 
        tempImage = self.result.copy()
        tempImage = tempImage.resize(Population.sourceSize, Image.ANTIALIAS)
        resultCalcDifference = 0
        resultCalcDifference = np.array(tempImage.convert("RGB").getdata()).reshape(tempImage.size[0], tempImage.size[1], 3) - Population.ndArraySource
        resultCalcDifference *=resultCalcDifference
        resultCalcDifference = resultCalcDifference.sum(axis = 2)
        resultCalcDifference = np.sqrt(resultCalcDifference)
        resultCalcDifference = resultCalcDifference.sum()
        if Population.bestMatch > resultCalcDifference:
            Population.bestMatch = resultCalcDifference
            Population.imageBigResult = self.result