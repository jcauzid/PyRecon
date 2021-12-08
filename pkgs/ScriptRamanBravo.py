# -*- coding: utf-8 -*-
from pkgs.CheckFeature import *
from PyRecon import *
import sys

global filename_RB, FilePath_RB, Result_RB
filename_RB = os.path.abspath(__file__)
##### DecisionTree :
DecisionTree_RB = pd.read_csv(os.getcwd() + os.path.sep + "pkgs" + os.path.sep + "Standards" + os.path.sep + "DecisionTrees" + os.path.sep +"Raman_Region.csv") 
##### Processing  :
ListFile = os.listdir(AdressFolder_RB)
name = os.path.splitext(ListFile[0])[0]
obj = Raman(AdressFolder=AdressFolder_RB,Name= name)
DF_RB = obj.Read_Interpolated_spectrums_()
ALL_DF_RB = [ DF_RB[[DF_RB.columns[0],DF_RB.columns[i]]] for i in range(1,len(DF_RB.columns))]
LV_RB = [0, 580, 850, 1200]
HV_RB = [580, 850, 1200,1600]
Result_failed_RB = []
def ProcessInput_RB(k):
    global result
    try :
        print("Processing of {} spectrum".format(ALL_DF_RB[k].columns[1][0]))
        ckf = CheckFeature(Tool = Tool_RB ,AdressFolder = AdressFolder_RB, SpecDataFrame = ALL_DF_RB[k], Name = ALL_DF_RB[k].columns[1][0], 
                                    DecisionTree  = DecisionTree_RB,
                                    LowValue = 0, HighValue = 2000, startContinuum=LV_RB, stopContinuum=HV_RB, 
                                    normalize=True, Scale = True, NumberShift = 2,
                                    Verbose = False)

        res, OBJ = ckf.Peaks()
        result = ckf.PeaksDataFrame(PeakPoints = res)
    except :
        print("============================, Result failed : ", ALL_DF_RB[k].columns[1][0])
        Result_failed_RB.append(ALL_DF_RB[k].columns[1][0])
        result = pd.DataFrame()
        pass 
    return result




print ("++++++++++++++++++++++++++++++++++++++++ The Raman Bravo process is started +++++++++++++++++++++++++++++++++++++++++++++")
list_result = []    
for k in range(len(ALL_DF_RB)): list_result.append(ProcessInput_RB(k)) 
list_filtred_result = sorted(list_result, reverse=True ,key=lambda list_filtred_result: len(list_filtred_result.columns))
Result_RB = pd.concat(list_filtred_result)
FilePath_RB = AdressFolder_RB +  os.path.sep +  "Results" +  os.path.sep+ "{}_feature_result.csv".format(Tool_RB)
Result_RB.to_csv(FilePath_RB)
print ("++++++++++++++++++++++++++++++++++++++++ The Raman Bravo process is finished ++++++++++++++++++++++++++++++++++++++++++++") 
