# -*- coding: utf-8 -*-
import os
import sys
from PyRecon import Run

global fileName, IdXrf

List_fileName = ["point1","point2","point3","point4","point5","point6","point7","point8","point9","point10"]
List_IdXrf    = [29, 34, 103, 576, 594, 597, 606, 633, 639, 798]

for k in range(len(List_fileName)):
    
    print(k) 
    Run(List_fileName, List_IdXrf, k)

#for fileName, IdXrf in zip(List_fileName,List_IdXrf):
#    toloop(fileName, IdXrf) 

#filename = os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "ReconciliationMatrix.py"
#exec(compile(open(filename).read()))
#exec(compile(open(filename).read(), filename, 'exec') )
#exec(compile(open(filename).read(), filename, 'exec') )
#from pkgs.ReconciliationMatrix import *