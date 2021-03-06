# -*- coding: utf-8 -*-
import numpy as np
import random as rnd
import time
import sys

from PIL import Image, ImageDraw, ImageFilter,ImageEnhance

class Population(object):
    """docstring for Population"""
    sourceSize = ()
    resultQuality = 1
    imageSource = ""
    ndArraySource = ""
    imageBigResult = ""
    bestMatch = 100000000
    @staticmethod
    def setImageSource(str):
        print("setImageSource()")
        Population.imageSource = Image.open(str).convert("RGB")
        Population.sourceSize = Population.imageSource.size[0], Population.imageSource.size[1]
        Population.ndArraySource = np.array(Population.imageSource.getdata()).reshape(Population.sourceSize[0], Population.sourceSize[1], 3)
        Population.imageBigResult = Image.new("RGBA", (Population.sourceSize[0]*Population.resultQuality, Population.sourceSize[1]*Population.resultQuality), (0,0,0,0))

    def __init__(self, numPrimitives=1):
        print("Population.__init__")
        self.resultSize = Population.sourceSize[0], Population.sourceSize[1]
        self.resultType = Population.imageSource.mode
        self.numPrimitives = numPrimitives
        self.resultQuality = Population.resultQuality
        self.resultBigSize = self.resultSize[0]*self.resultQuality, self.resultSize[1]*self.resultQuality
        self.best = False
        self.sizePrimitive = (self.resultBigSize[0], self.resultBigSize[1])
        self.positionPrimitive = [0, 0]

    def reset(self):
        print("reset()")
        self.result = Population.imageBigResult.copy()

    def paintPrimitive(self):
        print("paintPrimitive()")
        primitive= Image.new("RGBA", (self.resultBigSize[0], self.resultBigSize[1]), (0,0,0,0))
        drawPrimitive = ImageDraw.Draw(primitive)

        for cntTr in xrange(self.numPrimitives):
            self.positionPrimitive[0] = rnd.randint(0, self.resultBigSize[0] - self.sizePrimitive[0])
            self.positionPrimitive[1] = rnd.randint(0, self.resultBigSize[1] - self.sizePrimitive[1])
            x1, x2, x3 = rnd.sample(range(0, self.sizePrimitive[0]), 3)
            y1, y2, y3 = rnd.sample(range(0, self.sizePrimitive[1]), 3)
            color = tuple(rnd.sample(range(0, 255), 3))
            drawPrimitive.polygon((x1 + self.positionPrimitive[0], y1 + self.positionPrimitive[1], x2 + self.positionPrimitive[0], y2 + self.positionPrimitive[1], x3 + self.positionPrimitive[0], y3 + self.positionPrimitive[1]), outline=color, fill=color)
            opacity = 0.5
            self.addTriangle(primitive, opacity)

    def addTriangle(self, primitive, opacity):
        print("addTriangle()")
        if opacity < 1:
            alpha = primitive.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            primitive.putalpha(alpha)
        self.result = Image.alpha_composite(self.result, primitive)

    def calcDifference(self):
        print("calcDifference()")
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
            self.best = True

    def isBest(self):
        print("isBest()")
        return self.best