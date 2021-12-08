# -*- coding: utf-8 -*-
import os

List_fileName = ["point1","point2","point3","point4","point5","point6","point7","point8","point9","point10"]
List_IdXrf    = [29, 34, 103, 576, 594, 597, 606, 633, 639, 798]

fichierdebut = open("pyrecon-debut.txt", "r")
debut=fichierdebut.read()
fichierfin = open("pyrecon-fin.txt", "r")
fin=fichierfin.read()

bashstr = "#!/bin/bash\n"

for i in range(len(List_fileName)):
    outstr=debut+"\nfileName = \""+List_fileName[i]+"\"\nIdXrf = "+str(List_IdXrf[i])+"\n"+fin
    outfilename = "PyRecon.py"
    fichierpoint= open(outfilename, "w")
    fichierpoint.write(outstr)
    fichierpoint.close()
    os.system("python3 PyRecon.py")


