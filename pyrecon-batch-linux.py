#/*##########################################################################
# Copyright (C) 2020-2021 The University of Lorraine - France
#
# This file is part of the PyRecon toolkit developed at the GeoRessources
# Laboratory of the University of Lorraine, France.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/

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


