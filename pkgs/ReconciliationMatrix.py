# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import sys
from PyRecon import *
from pkgs.ElementaryQuantyficationProportion import *

global Matrix, Vector, Errors


MatrixFilePath = os.path.abspath(__file__)

def VraiSemblance(Sample,Density,Matrix,Errors):
    """
    
    """
    C =  np.eye(len(Errors),len(Errors))*1/Errors
    V = np.dot(Matrix,Sample) - Density.reshape(np.shape(Matrix)[0],1)
    P = np.dot(np.dot(np.transpose(V),C),V)
    result = (1/np.sqrt(2*np.pi))*np.exp(-0.5*P[0][0])
    return result
def Sampling(Density,Matrix,Errors): 
    """
    
    """
    SamplSize = 10000 * np.shape(Matrix)[1]
    Samples = list()
    for k in range(SamplSize):
        prop = np.random.rand(np.shape(Matrix)[1],1)
        if np.sum(prop) <= 1.2:
            Samples.append(prop)
    Likelyhood = [VraiSemblance(Sample,Density,Matrix,Errors) for Sample in Samples]
    return Likelyhood, Samples
    
def MaximumLikelyhood(DF_Matrix,Density,Matrix,Errors):
    """
    
    """
    Likelyhood, Samples = Sampling(Density = Density,Matrix = Matrix,Errors = Errors)
    idx_max_likelyhood  = Likelyhood.index(np.max(Likelyhood))
    Concentration = pd.DataFrame(data = Samples[idx_max_likelyhood] , index = DF_Matrix.columns)
    Concentration.rename(columns = {Concentration.columns[0] : "Concentration"}, inplace = True)
    Concentration.to_csv(os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + "Concentration.csv")
    #print("Maximum of Likelyhood is : ", np.max(Likelyhood))
    for k in range(len(DF_Matrix.columns)): 
        print("Concentration of {} ".format(DF_Matrix.columns[k]), Samples[idx_max_likelyhood][k])
########################################################### Pre Matrix #######################################################
AdressPreMatrix = os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" + os.path.sep + "mineralogical database-LIB-ELV.xlsx"
AdressDataXrf = os.getcwd() + os.path.sep + "pkgs" + os.path.sep +  "Standards" + os.path.sep + "xrf.xls"

####### Raman Bravo #######
from pkgs.ScriptRamanBravo import *
####### Raman Rapport #######
from pkgs.ScriptRamanRaPort import *
####### Venir Swir  #######
from pkgs.ScriptVnirSwir  import *
########################################################### Pre Matrix #######################################################
Result = pd.concat([Result_RB, Result_RR, Result_VS]) 


if not Result.empty:
    Result = pd.concat([Result_RB, Result_RR, Result_VS]) 
    Result = Result.dropna(axis=0, how='all')
    Result = Result.sort_values(by = ['Mineral','Tool'], ascending=False)
    ## Raman Bravo : 
    Condition_RB   =  (Result.index.get_level_values(2) == Tool_RB) & (Result.index.get_level_values(1) < 800)
    indices = Result[Condition_RB].index 
    if not indices.empty : Result.drop(indices , inplace=True)
    ## Raman Rapport :
    Condition_RR   =  (Result.index.get_level_values(2) == Tool_RR) & (Result.index.get_level_values(1) < 1500)
    indices = Result[Condition_RR].index 
    if not indices.empty : Result.drop(indices , inplace=True)
    ## Vnir Swir : 
    Condition_VS   =  (Result.index.get_level_values(2) == Tool_VS) & (Result.index.get_level_values(1) < 13)
    indices = Result[Condition_VS].index 
    if not indices.empty : Result.drop(indices , inplace=True)
    #### Select Carbonate and Chlorite :
    # Carbonate :
    try :
        Condition_Carbonate = (Result.index.get_level_values(-1) == "Carbonate") & (Result.index.get_level_values(2) == 'Raman-Bravo')
        indices_Carbonate = Result[Condition_Carbonate].index
        Condition_Carbonate_Max = (Result.index.get_level_values(1) == max(Result.loc[indices_Carbonate].index.get_level_values(1).values))
        Id_Carbonate = Result.loc[Condition_Carbonate_Max].index
        if len(list(Id_Carbonate)) == 0 :
            Condition_Carbonate = (Result.index.get_level_values(-1) == "Carbonate") & (Result.index.get_level_values(2) == 'Raman-RaPort')
            indices_Carbonate = Result[Condition_Carbonate].index
            Condition_Carbonate_Max = (Result.index.get_level_values(1) == max(Result.loc[indices_Carbonate].index.get_level_values(1).values))
            Id_Carbonate = Result.loc[Condition_Carbonate_Max].index
    except : 
        print("The Carbonate doesn't exist in this sample ")
        pass 
    # Chlorite :
    try :
        Condition_Chlorite = (Result.index.get_level_values(-1) == "Chlorite")
        indices_Chlorite = Result[Condition_Chlorite].index
        Condition_Chlorite_Max = (Result.index.get_level_values(1) == max(Result.loc[indices_Chlorite].index.get_level_values(1).values))
        Id_Chlorite = Result.loc[Condition_Chlorite_Max].index
    except : 
        print("The Chlorite doesn't exist in this sample ")
        pass 
    ### Saving the PreMatrix :
    ########################################################### Minerals Resulting #######################################################
    Minerals_ = []
    for m in list(Result.index.get_level_values(-1)):
        if m not in Minerals_:
            Minerals_.append(m)
    Minerals_ = [MINERALS.upper() for MINERALS in Minerals_ ]
    ###########################################################  Reconciliation Matrix and Elements #######################################################
    PreMatrix = pd.read_excel(AdressPreMatrix)
    PreMatrix = PreMatrix[13::]
    Matrix = PreMatrix[PreMatrix.columns[9::2]][3::]
    Matrix.index =  PreMatrix[PreMatrix.columns[2]][3::].str.upper()
    Matrix.columns = ["Mg","Al","Si","P","S","K","Ca","Ti","Mn","Fe","Cu","Zn","Ba","P"]
    if 'Id_Carbonate' in locals():
        if "CARBONATE" in Matrix.index : Matrix.drop(["CARBONATE"] , inplace=True)
        Id_Carbonate = Id_Carbonate[0]
        AdressFolder = os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + Id_Carbonate[2] #+ os.path.sep + Id_Carbonate[0]
        RefFolder    = RefFolder + os.path.sep + Id_Carbonate[2]
        
        if  Id_Carbonate[2] == "Raman-RaPort"  : 
            valinf = [153 ,167 ,171 ,181 ,209]
            valsup = [156 ,171 ,178 ,192 ,213] 
        if  Id_Carbonate[2] == "Raman-Bravo"    : 
            valinf = [710 ,718 ,721 ,726 ,734]
            valsup = [714 ,722 ,726 ,732 ,738] 
        
        obj = ElementaryQuantyficationProportion(AdressFolder = AdressFolder, nameSpectra = Id_Carbonate[0], AdressRefFolder = RefFolder,
                                                 AdressDensitisFolder = Densities, AdressCompositionFolder = CompositionFolder,
                                                 valinf = valinf, valsup = valsup 
                                                 )
        Carbonate = obj.CarbonateElementaryProportion()
        Matrix = Matrix.append(Carbonate)
    if 'Id_Chlorite' in locals():
        if "CHLORITE"  in Matrix.index : Matrix.drop(["CHLORITE"] , inplace=True)
        Id_Chlorite = Id_Chlorite[0]
        DF_     = Result.loc[Condition_Chlorite_Max]
        cond    = DF_.columns[DF_.columns.get_level_values(1) == 'Peak position']
        DF_     =  DF_[list(cond)]
        obj = ElementaryQuantyficationProportion()
        if not np.isnan(max(DF_[DF_.columns[1]].values))    :
            x = max(DF_[DF_.columns[1]].values)
            CHRT = obj.Chlorite_Raman(x)
        elif not np.isnan(max(DF_[DF_.columns[4]].values))  :
            x = max(DF_[DF_.columns[4]].values)
            CHRT = obj.Chlorite_Raman(x)
        elif not np.isnan(max(DF_[DF_.columns[7]].values))  :
            x = max(DF_[DF_.columns[7]].values)
            CHRT = obj.Chlorite_VNIR_SWIR(x)
        Matrix = Matrix.append(CHRT)
    PreVector =  pd.read_excel(AdressDataXrf)
    condition = PreVector[PreVector.columns[1]] == IdXrf
    ligne = PreVector[condition]
    PreVector = ligne[ligne.columns[13::2]]
    PreErrors = ligne[ligne.columns[14::2]]
    PreVector = PreVector.replace(r'^\s*$', np.NaN, regex=True)
    PreVector = PreVector._get_numeric_data()
    ################ Select rows from Matrix : 
    Minerals = []
    for m in Minerals_:
        if m in Matrix.index:
            Minerals.append(m)
    if len(Minerals) >=2:
        print("########################################### The Process of Reconciliation is started ###########################################")
        Matrix = Matrix.loc[Minerals]
        Matrix = Matrix.transpose()
        Matrix = Matrix.dropna()
        Elements = list(Matrix.index)
        ElementsToChek = []
        for e in Elements:
            if e in PreVector.columns:
                ElementsToChek.append(e)       
        # Matrix :
        Matrix = Matrix.loc[ElementsToChek]
        Matrix.to_csv(os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + "Matrix.csv")
        print("The Matrix is    :\n", Matrix)
        DF_Matrix = Matrix
        Matrix = Matrix.values
        # Vector :
        PreVector = PreVector[ElementsToChek].transpose()
        PreVector.to_csv(os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + "Vector.csv")
        Vector = PreVector.values
        print("The Vector is    :\n",  PreVector)
        # Errors :
        ErrorElementsToChek = [e + " Error" for e in ElementsToChek]
        Errors = PreErrors[ErrorElementsToChek].transpose()
        Errors.to_csv(os.getcwd() + os.path.sep + "Spectra" + os.path.sep + fileName + os.path.sep + "Errors.csv")
        print("The Errors are   :\n", Errors)
        Errors = Errors.values
        ####  Concentration (Solving the inverse problem)  : 
        MaximumLikelyhood(DF_Matrix = DF_Matrix ,Density =  Vector ,Matrix = Matrix ,Errors = Errors)
    else : 
        #Matrix = pd.DataFrame()
        print("The number of minerals detected is not sufficient")
        print("Only {} is detected ".format(Minerals))
else : 
    print("The number of minerals detected is not sufficient")

