# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import os
import re
import json
import logging
import collections

class SpectraPreProcessing(object):  
    
    def __init__(self, AdressFolder):
        self.AdressFolder = AdressFolder
        self.AllFiles = os.listdir(self.AdressFolder)


    def FileExtension(self,Name): 
        ''' 
        Return the file extension 
        '''
        Names = [os.path.splitext(self.AllFiles[i])[0] for i in range(len(self.AllFiles))]
        Extension = os.path.splitext(self.AllFiles[Names.index(Name)])[1]
        return  Extension

    def FilePath(self,Name): 
        ''' 
        Return the adress file 
        '''
        AdressFile = self.AdressFolder + os.path.sep + Name + self.FileExtension(Name)
        return AdressFile

    def Extensions(self):
        ''' 
        Return extensions existing in the folder

        Note: sometimes we find different extensions for the same spectral analysis hence the usefulness of this function 
        '''
        List_of_extentions = [os.path.splitext(self.AllFiles[i])[1] for i in range(len(self.AllFiles))]
        extensions = [item for item, count in collections.Counter(List_of_extentions).items()if count > 1]
        #extensions = [item for item, count in collections.Counter(List_of_extentions).items() if count > 1]
        return extensions

    def NameFiles(self):
        ''' 
        Return all file names in the folder even if they have different extensions
        '''
        li = []
        Names = self.AllFiles
        for adress in Names:
            for i in range(len(self.Extensions())):
                if adress.endswith(self.Extensions()[i]):
                    li.append(adress)
        Names = [os.path.basename(os.path.splitext(li[i])[0]) for i in range(len(li))]
        return Names
    
    def Dict_to_Df(self, Dict):
        ''' 
        Transform Python dictionary to Pandas Data Frame
        '''
        df = pd.DataFrame([Dict.values()], columns=Dict.keys())
        return df
   
    def Save_as_csv(self, df, name):
        '''
        Save DataFrame as .csv in the same address folder 

        Note : Please enter the name of the .csv file as "name"
        '''
        df.to_csv(self.AdressFolder + os.path.sep + name + ".csv",header = True, index = False)
         
    def Add_columns(self, df, nameColumn, Value):
        ''' 
        Add a given columns to the data frame df 
        '''
        N_df = pd.DataFrame(data = {nameColumn : [Value]})
        df = self.Join_df(N_df,df)
        return df 

    def Join_df(self, df1, df2):
        ''' 
        Joins two DataFrames df1 and df2 
        '''
        df = df1.join(df2)
        return df

    def Count_Hachtags(self,Name):
        ''' 
        Returns the number of the Hachtags in the first "MaxLine" lines in the .txt or .esp files 

        Note : Useful for Raman Spectrums, where the header lines are detected by an Hashtags
        '''
        cnt = 0
        MaxLine = 50
        with open(self.FilePath(Name),'r') as f:
            for sent in f.readlines()[0:MaxLine]:
                if sent.startswith("#"):
                    cnt += 1
        return cnt

    def FindWord(self,Word,Name):
        ''' 
        Returns the number of lines before the line where is "Word" 

        Note : Useful for VNIR-SWIR Spectrums, where the header lines are detected by before the word "Data:"
        '''
        MaxLine = 50
        LineNum = 0
        with open(self.FilePath(Name),'r') as f:
            Text = f.readlines()[0:MaxLine]
            for i in range(len(Text)):
                if "Data:" in Text[i].rstrip():
                    LineNum = i
                    break
        return LineNum

    def Separator(self, Extension):
        ''' 
        Return the separator in the file

        Note : The separators are the distinction of columns when reading with Python, each extension has the one separator (ex : "," , "\t" or space).
        '''
        global Sep
        if Extension == ".csv":
            Sep =  ","
        elif Extension in [".0",".sed"]:
            Sep =  "\t"
        elif Extension in [".esp"]:
            Sep =  " "
        elif Extension in [".txt", ".TXT"] :
            with open(self.FilePath(self.Name)) as f:
                text = f.readlines()[0]
                if (text.find(",") != -1):
                    Sep = ","
                elif (text.find("\t") != -1):
                    Sep = "\t"
                elif (text.find(" ") != -1):
                    Sep = " "   
        return Sep

    def NameColumn(self,SampleName,ColomnName):
        ''' 
        Retrns a tuple

        Note : used to name the columns as a multilevel 
        '''
        li = [SampleName]
        [li.append(w) for w in ColomnName]
        return tuple(li)
    

    def X_DataFrame(self,list_of_DataFrames, NameFirstColumns):
        '''
        Returns Data frame containing the X_value from all spectrums without repetitions

                > list_of_DataFrames : List containing all spectrums Data Frame.
                > NameFirstColumns : is the name of the columns, for example "NumberWaves" must have the same level as sample names.

        '''
        List = list()
        # Collecting in "List" all the first columns of data frames in the  "list_of_DataFrames"
        for i in range(len(list_of_DataFrames)):
            List += list_of_DataFrames[i][list_of_DataFrames[i].columns[0]].to_list()
        
        # Collecting the repeated elements in "List"
        RE = [item for item, count in collections.Counter(List).items()]
        RE = np.sort(RE)
        # Creating DataFrame with "RE" (Repeated Element)
        df = pd.DataFrame({NameFirstColumns :RE})
        return df

    def FindIndex(self,XDataFrame,ValuesToCollect):
        ''' 
        Returns the position Values in the X _ Data Frame

                > XDataFrame :  Data Frame generated by the function "X_DataFrame".
                > ValuesToCollect : The columns containig the values.
        '''
        global Index
        index = XDataFrame.index
        condition = XDataFrame[XDataFrame.columns[0]] == ValuesToCollect
        indices = index[condition]
        indices = indices.tolist()
        try:
            Index = indices[0]
        except IndexError:
            print("The parameter ' {} ' doesn't exist in the parameter colomn.".format(ValuesToCollect))
            Index = np.nan
        return Index
        
    def ExtractRegion(self,DataFrame, LowValue, HighValue):
        ''' 
        Returns a region from "DataFrame" between LowValue and HighValue :  LowValue  <= DataFrame <= HighValue
        '''
        if LowValue is None and HighValue is None:
            return DataFrame
        elif LowValue is None and HighValue is not None:
            DF = DataFrame.loc[(DataFrame[DataFrame.columns[0]] <= HighValue)]
            return DF
        elif LowValue is not None and HighValue is  None:
            DF = DataFrame.loc[(DataFrame[DataFrame.columns[0]] >= LowValue)]
            return DF
        else :
            DF = DataFrame.loc[(DataFrame[DataFrame.columns[0]] <= HighValue) & (DataFrame[DataFrame.columns[0]] >= LowValue)]
            return DF
    
    def SpecScale(self,DataFrame,NumberShift):
        ''' 
        Returns Data Frame transformed, for using the hull quotient in PySpTools.
        '''
        DF = DataFrame.copy()
        maxColumn = DF[DF.columns[1]].max()
        DF.loc[:, DF.columns[1]] = (-1)*DF[DF.columns[1]].values + NumberShift*maxColumn


        return DF

    




 

