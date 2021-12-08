# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os

############################# Raman ####################################
Group = ["Silicate","Silicate","Silicate","Silicate","Silicate","Silicate","Carbonate","Graphite","Sulfate","Sulfate","Sulfide","Sulfide","Sulfide","Sulfide","Sulfide","Sulfide"]
Subgroup = ["Tectosilicate","Tectosilicate","Tectosilicate","Tectosilicate","Phyllosilicate","Phyllosilicate","Carbonate","Graphite","Barite","Gypsum","Pyrite","Sphalerite","Chalcopyrite","Chalcopyrite","Pyrrhotite","Pyrrhotite"]
Mineral  = ["Anorthite","Albite", "Orthoclase","Quartz","Muscovite","chlorite" ,"Carbonate","Graphite","Barite","Gypsum","Pyrite","Sphalerite","Chalcopyrite","Chalcopyrite","Pyrrhotite","Pyrrhotite"]

Raman_Region_1_Min = [504, 505, 510, 463, 700, 546, 1085, 1580, 986, 1006, 340, 346, 415, 289, 415, 373]
Raman_Region_1_Max = [508, 509, 514, 467, 704, 552, 1100, 1600, 990, 1008, 345, 350, 418, 292, 418, 375]

Raman_Region_2_Min = [480, 476, 472, 352, 404, 655, 712,  None, 456, 490, 375, 416, None, 350, 378, 338]
Raman_Region_2_Max = [484, 480, 475, 358, 413, 685, 742,  None, 462, 494, 380, 420, None, 354, 386, 340]

Raman_Region_3_Min = [None,  None,  None, 392,  None,  None, 155,  None,  None, 412,  None, 666,  None, 317,  None, 422]
Raman_Region_3_Max = [None,  None,  None, 400,  None,  None, 215,  None,  None, 415,  None, 672,  None, 321,  None, 426]



DF = pd.DataFrame({"Group" : Group,
                    "Subgroup" : Subgroup,
                    "Mineral" : Mineral,
                    "Raman_Region_1_Min" : Raman_Region_1_Min,
                    "Raman_Region_1_Max" : Raman_Region_1_Max,
                    "Raman_Region_2_Min" : Raman_Region_2_Min,
                    "Raman_Region_2_Max" : Raman_Region_2_Max,
                    "Raman_Region_3_Min" : Raman_Region_3_Min,
                    "Raman_Region_3_Max" : Raman_Region_3_Max
                    }, dtype= np.float
                    )

DF.to_csv("Raman_Region.csv")
dfDT_Rmn = pd.read_csv("Raman_Region.csv" ) 


############################# Venir_Swir ####################################
Group  = ["Silicate","Silicate","Silicate","Silicate","Silicate", "Carbonate"] 
Subgroup = ["Phyllosilicate","Phyllosilicate","Phyllosilicate","Phyllosilicate","Phyllosilicate", "Carbonate"]
Mineral  = ["Kaolinite","Muscovite","Montmorillonite","Chlorite","Nontronite", "Carbonate"]

Venir_Swir_Region_1_Min = [2205, 2185, 1900, 2320, 1900, 2300]
Venir_Swir_Region_1_Max = [2210, 2225, 1915, 2360, 1915, 2340]

#Venir_Swir_Region_1_Min = [2207, 2196, 1902, 2335, 1907, 2300]
#Venir_Swir_Region_1_Max = [2209, 2208, 1910, 2343, 1909, 2340]

Venir_Swir_Region_2_Min = [2160, 1405, 2202, 2240, 1410, None]
Venir_Swir_Region_2_Max = [2170, 1415, 2212, 2260, 1460, None]

#Venir_Swir_Region_2_Min = [2162, 2438, 2205, 2250, 2284, None]
#Venir_Swir_Region_2_Max = [2164, 2440, 2210, 2260, 2288, None]

Venir_Swir_Region_3_Min = [1410, 2345, 1405, 1390, 2270, None]
Venir_Swir_Region_3_Max = [1420, 2355, 1420, 1410, 2296, None]

#Venir_Swir_Region_3_Min = [1413, 2347, 1411, 1393, 2400, None]
#Venir_Swir_Region_3_Max = [1415, 2352, 1414, 1399, 2404, None]

Venir_Swir_Region_4_Min = [1390, 2430, None, None, 2363, None]
Venir_Swir_Region_4_Max = [1400, 2440, None, None, 2394, None]

#Venir_Swir_Region_4_Min = [1393, 1409, None, None, 1432, None]
#Venir_Swir_Region_4_Max = [1395, 1412, None, None, 1436, None]


DF = pd.DataFrame({"Group" : Group,
                    "Subgroup" : Subgroup,
                    "Mineral" : Mineral,
                    "Venir_Swir_Region_1_Min" : Venir_Swir_Region_1_Min,
                    "Venir_Swir_Region_1_Max" : Venir_Swir_Region_1_Max,
                    "Venir_Swir_Region_2_Min" : Venir_Swir_Region_2_Min,
                    "Venir_Swir_Region_2_Max" : Venir_Swir_Region_2_Max,
                    "Venir_Swir_Region_3_Min" : Venir_Swir_Region_3_Min,
                    "Venir_Swir_Region_3_Max" : Venir_Swir_Region_3_Max
                    }, dtype= np.float
                    )

DF.to_csv("Venir_Swir_Region.csv")
dfDT_VS = pd.read_csv("Venir_Swir_Region.csv") 

############################# IR ####################################


Group = ["Silicate","Silicate","Silicate","Silicate","Silicate","Silicate","Carbonate","Graphite","Sulfate" ,"Sulfate"] 
Subgroup = ["Tectosilicate","Tectosilicate","Tectosilicate","Tectosilicate","Phyllosilicate","Phyllosilicate","Carbonate","Graphite","Barite" ,"Gypsum"] 
Mineral  = ["Anorthite","Albite","Orthoclase","Quartz","Muscovite","Chlorite","Carbonate","Graphite","Barite" ,"Gypsum"] 


IR_Region_1_Min = [535, 1000, 1110, 1095, 1035, 1015, 1525, 990, 605, 1140]
IR_Region_1_Max = [545, 1010, 1120, 1115, 1050, 1025, 1570, 1015, 615, 1160]

#IR_Region_1_Min = [538, 1002, 1112, 1096, 1040, 1016, 1530, 1000, 608, 1147]
#IR_Region_1_Max = [541, 1006, 1118, 1116, 1044, 1024, 1568, 1006, 610, 1153]

IR_Region_2_Min = [940, 1030, 1235, 1205, 540, 550, 1410, 1075, 1085, 665]
IR_Region_2_Max = [950, 1040, 1245, 1215, 555, 560, 1445, 1095, 1115, 680]


#IR_Region_2_Min = [942, 1035, 1236, 1200, 545, 550, 1416, 1083, 1094, 671]
#IR_Region_2_Max = [950, 1039, 1240, 1210, 551, 553, 1442, 1088, 1097, 676]

IR_Region_3_Min = [630, 595, 595, 535, 1095, 645, 875, None, 1105, 595]
IR_Region_3_Max = [640, 605, 605, 550, 1110, 660, 900, None, 1125, 615]

IR_Region_4_Min = [990, 530, 530, 775, 740, 745, None, None, 630, 1615]
IR_Region_4_Max = [1100, 540, 540, 785, 755, 760, None, None, 645, 1625]
'''
IR_Region_5_Min = [598, 1146, 574, 798, 792, 824, None, None, 1212, 1618]
IR_Region_5_Max = [602, 1149, 580, 800, 798, 826, None, None, 1216, 1621]


IR_Region_6_Min = [573, 1180, 559, None, None, 1189, None, None, 978, None]
IR_Region_6_Max = [576, 1186, 563, None, None, 1192, None, None, 982, None]
'''
IR_Region_5_Min = [None, None, None, 795, 790, None, None, None, 1205, None]
IR_Region_5_Max = [None, None, None, 805, 800, None, None, None, 1225, None]





DF = pd.DataFrame({"Group" : Group,
                    "Subgroup" : Subgroup,
                    "Mineral" : Mineral,
                    "IR_Region_1_Min" : IR_Region_1_Min,
                    "IR_Region_1_Max" : IR_Region_1_Max,
                    "IR_Region_2_Min" : IR_Region_2_Min,
                    "IR_Region_2_Max" : IR_Region_2_Max,
                    "IR_Region_3_Min" : IR_Region_3_Min,
                    "IR_Region_3_Max" : IR_Region_3_Max,
                    "IR_Region_4_Min" : IR_Region_4_Min,
                    "IR_Region_4_Max" : IR_Region_4_Max,
                    "IR_Region_5_Min" : IR_Region_5_Min,
                    "IR_Region_5_Max" : IR_Region_5_Max
                    #"IR_Region_6_Min" : IR_Region_6_Min,
                    #"IR_Region_6_Max" : IR_Region_6_Max
                    }, dtype= np.float
                    )

DF.to_csv("IR_Region.csv")
dfDT_IR = pd.read_csv("IR_Region.csv") 

