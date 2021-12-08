# -*- coding: utf-8 -*-
import os
import sys





def GlobalVariabls(k): 

    global AdressFolder_RB, Tool_RB, AdressFolder_RR, Tool_RR, AdressFolder_VS, Tool_VS, fileName, IdXrf, Folder, CompositionFolder, RefFolder, Densities


    List_fileName = ["point1","point2","point3","point4","point5","point6","point7","point8","point9","point10"]
    List_IdXrf    = [29, 34, 103, 576, 594, 597, 606, 633, 639, 798]

    fileName = List_fileName[k]
    IdXrf    = List_IdXrf[k]

    Tool_RR = "Raman-RaPort"
    AdressFolder_RR = os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + Tool_RR

    Tool_RB = "Raman-Bravo"
    AdressFolder_RB = os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + Tool_RB

    Tool_VS = "VNIR-SWIR"
    AdressFolder_VS = os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + Tool_VS


    Folder              = os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" 
    CompositionFolder   = Folder + os.path.sep + "Compositions"
    RefFolder           = Folder + os.path.sep + "References" 
    Densities           = Folder + os.path.sep + "Densities" + os.path.sep + "Ref-mineral-densities.csv"


def Run():
    import pkgs.ReconciliationMatrix
    del AdressFolder_RB, Tool_RB, AdressFolder_RR, Tool_RR, AdressFolder_VS, Tool_VS, fileName, IdXrf, Folder, CompositionFolder, RefFolder, Densities
    


for k in [0,1,3]:
    GlobalVariabls(k)
    Run()
    #del AdressFolder_RB, Tool_RB, AdressFolder_RR, Tool_RR, AdressFolder_VS, Tool_VS, fileName, IdXrf, Folder, CompositionFolder, RefFolder, Densities


    

    









        
        
    


    
    


