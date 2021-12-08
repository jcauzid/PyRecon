# -*- coding: utf-8 -*-
from pkgs.CheckFeature import *
from PyRecon import *
import sys

#################### Global variables :
global filename_RR, FilePath_RR, Result_RR
filename_RR = os.path.abspath(__file__)
##### DecisionTree :
DecisionTree_RR = pd.read_csv(os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" + os.path.sep + "DecisionTrees" + os.path.sep + "Raman_Region.csv") 
##### Processing  :
ListFile = os.listdir(AdressFolder_RR)
name = os.path.splitext(ListFile[0])[0]
obj = Raman(AdressFolder=AdressFolder_RR,Name= name)
DF_RR = obj.Read_Interpolated_spectrums_()
ALL_DF_RR = [ DF_RR[[DF_RR.columns[0],DF_RR.columns[i]]] for i in range(1,len(DF_RR.columns))]
LV_RR = [0, 580, 850, 1200]
HV_RR = [580, 850, 1200,1600]
Result_failed_RR = []
def ProcessInput_RR(k):
    global result, Result_RR
    try :
        print("Processing of {} spectrum".format(ALL_DF_RR[k].columns[1][0]))
        ckf = CheckFeature(Tool = Tool_RR ,AdressFolder = AdressFolder_RR, SpecDataFrame = ALL_DF_RR[k], Name = ALL_DF_RR[k].columns[1][0], 
                                    DecisionTree  = DecisionTree_RR,
                                    LowValue = 0, HighValue = 2000, startContinuum=LV_RR, stopContinuum=HV_RR, 
                                    normalize=True, Scale = True, NumberShift = 2,
                                    Verbose = False)

        res, OBJ = ckf.Peaks()
        result = ckf.PeaksDataFrame(PeakPoints = res)        
    except :
        print("============================, Result failed : ", ALL_DF_RR[k].columns[1][0])
        Result_failed_RR.append(ALL_DF_RR[k].columns[1][0])
        result = pd.DataFrame()
        pass 
    return result


print ("++++++++++++++++++++++++++++++++++++++++ The Raman Rapport process is started +++++++++++++++++++++++++++++++++++++++++++")
DecisionTree_RR = pd.read_csv(os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" + os.path.sep + "DecisionTrees" + os.path.sep + "Raman_Region.csv") #
list_result = []
for k in range(len(ALL_DF_RR)): list_result.append(ProcessInput_RR(k)) 
list_filtred_result = sorted(list_result, reverse=True ,key=lambda list_filtred_result: len(list_filtred_result.columns))
Result_RR = pd.concat(list_filtred_result)
FilePath_RR = AdressFolder_RR +  os.path.sep+  "Results" +  os.path.sep+ "{}_feature_result.csv".format(Tool_RR)
Result_RR.to_csv(FilePath_RR)
print ("++++++++++++++++++++++++++++++++++++++++ The Raman Rapport process is finished ++++++++++++++++++++++++++++++++++++++++++")

