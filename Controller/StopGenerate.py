# -*- coding: utf-8 -*-
__author__ = 'Dmitry Sapronov'
from Controller import *

class StopGenerate(Controller):
        def Action(self):
            self.model.stopCalc()