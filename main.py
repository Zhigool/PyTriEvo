# -*- coding: utf-8 -*-
__author__ = 'Dmitry Sapronov'

import sys
from Model.Model import *
from View.View import *
from Controller.BttnOpenFile import *
from Controller.BttnStop import *
from Controller.BttnContinue import *
from Controller.BttnSaveProgress import *
from Controller.BttnSaveResult import *
from Controller.Generate import *
from Controller.StopGenerate import *

def main():

    model = Model()

    controllers = {}
    controllers["bttn_openFile"] = BttnOpenFile(model)
    controllers["bttn_generate"] = Generate(model)
    controllers["bttn_stop"] = StopGenerate(model)

    view = View()

    model.addView(view)

    view.addControllers(controllers)

    view.startloop()



if __name__ == '__main__':
    sys.exit(main())
