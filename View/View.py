# -*- coding: utf-8 -*-
__author__ = 'Dmitry Sapronov'

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename, askopenfile

from PIL import Image, ImageTk

class View():
    def __init__(self):
        print("View.__init__")
        self.root = Tk()
        self.root.title("PyTriEvo")

        self.frame = Frame(self.root)
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.lbl1 = Label(self.frame)
        self.lbl1.grid(row = 0, column = 0, sticky=(N, W, E, S))

        self.lbl2 = Label(self.frame)
        self.lbl2.grid(row = 0, column = 1, sticky=(N, W, E, S))

        self.bttn_openFile = Button(self.frame, text = "Open file", width = 15)
        self.bttn_openFile.grid(row = 1, column = 0, sticky=(N, W, E, S))

        self.bttn_generate = Button(self.frame, text = "Generate", width = 15)
        self.bttn_generate.grid(row = 1, column = 1, sticky=(N, W, E, S))

    def addControllers(self, controllers):
        print("addControllers")
        self.controllers = controllers
        for cnt in self.controllers:
            if cnt == "bttn_openFile":
                self.bttn_openFile['command'] = controllers['bttn_openFile'].Action
            elif cnt == "bttn_generate":
                self.setGeneratBttnAsGenerate()

    def setGeneratBttnAsGenerate(self):
        print("setGeneratBttnAsGenerate()")
        self.bttn_generate["text"] = "Generate"
        self.bttn_generate["command"] = self.controllers['bttn_generate'].Action

    def setGeneratBttnAsStop(self):
        print("setGeneratBttnAsStop()")
        self.bttn_generate["text"] = "Stop"
        self.bttn_generate["command"] = self.controllers['bttn_stop'].Action

    def openFile(self):
        print("openFile()")
        nameFile = askopenfilename(filetypes=[("Image files", "*.png"), ("All files", ".*")])
        self.nameFile = Image.open(nameFile)
        self.nameFile = ImageTk.PhotoImage(self.nameFile)
        self.lbl1 = Label(self.frame, image = self.nameFile)
        self.lbl1['image'] = self.nameFile
        self.lbl1.grid(row = 0, column = 0, sticky=(N, W, E, S))
        return nameFile

    def saveFile(self):
        print("saveFile()")
        return asksaveasfilename(filetypes=(("Image files", "*.jpeg;*.png"), ("All files", "*.*")), initialfile="Untitled.jpeg")

    def updateImage(self, newImage):
        print("updateImage()")
        self.image = ImageTk.PhotoImage(newImage)
        self.lbl2["image"] = self.image
        self.lbl2.grid(row = 0, column = 1, sticky=(N, W, E, S))

    def startloop(self):
        print("startloop()")
        self.root.mainloop()