# -*- coding: utf-8 -*-
from pkgs.CheckFeature import *
from PyRecon import *
import sys

#################### Global variables :
global filename_VS, FilePath_VS, Result_VS
filename_VS = os.path.abspath(__file__)
##### DecisionTree :
DecisionTree_VS = pd.read_csv(os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" + os.path.sep + "DecisionTrees" + os.path.sep +"Venir_Swir_Region.csv") 
##### Processing  :
ListFile = os.listdir(AdressFolder_VS)
name = os.path.splitext(ListFile[0])[0]
obj = VNIR_SWIR(AdressFolder=AdressFolder_VS,Name= name)
DF_VS = obj.Read_spectrums()
ALL_DF_VS = [ DF_VS[[DF_VS.columns[0],DF_VS.columns[i]]] for i in range(1,len(DF_VS.columns))]
LV_VS = [1200, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300]
HV_VS = [1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]
Result_failed_VS = []
#results_VS = []
def ProcessInput_VS(k):
    global result
    try :
        print("Processing of {} spectrum".format(ALL_DF_VS[k].columns[1][0]))
        ckf = CheckFeature(Tool = Tool_VS ,AdressFolder = AdressFolder_VS, SpecDataFrame = ALL_DF_VS[k], Name = ALL_DF_VS[k].columns[1][0], 
                                    DecisionTree  = DecisionTree_VS,
                                    LowValue = None, HighValue = None, startContinuum=LV_VS, stopContinuum=HV_VS, 
                                    normalize=False, Scale = False, NumberShift = 2,
                                    Verbose = False)

        res, OBJ = ckf.Peaks()
        result = ckf.PeaksDataFrame(PeakPoints = res)
    except :
        print("============================, Result failed : ", ALL_DF_VS[k].columns[1][0])
        Result_failed_VS.append(ALL_DF_VS[k].columns[1][0])
        result = pd.DataFrame()
        pass 
    return result



    

print ("++++++++++++++++++++++++++++++++++++++++ The Vnir Swir process is started +++++++++++++++++++++++++++++++++++++++++++++++")
list_result = []  
for k in range(len(ALL_DF_VS)): list_result.append(ProcessInput_VS(k)) 
Result_VS = pd.concat(list_result, axis = 0, levels=1)
index = Result_VS.index
df = Result_VS.iloc[:, Result_VS.columns.get_level_values(1)=='Depth']
condition = (df[df.columns[0]] > 0.99) & (df[df.columns[1]] > 0.99)
indices = index[condition]
indices = indices.get_level_values(0)
FilePath_VS = AdressFolder_VS +  os.path.sep+  "Results" +  os.path.sep+ "{}_feature_result.csv".format(Tool_VS)
Result_VS.to_csv(FilePath_VS)
print ("++++++++++++++++++++++++++++++++++++++++ The Vnir Swir process is finished ++++++++++++++++++++++++++++++++++++++++++++++")

