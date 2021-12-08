# -*- coding: utf-8 -*-
from pkgs.SpectraPreProcessing import *
import numpy as np 
import pandas as pd
import re


'''
Once the object is built :              Obj = VNIR_SWIR(AdressFolder, Name)

Where :
        > AdressFolder : The path to the folder containing the files.
        > Name : the file name without the extension (ex : SR-6500_SN2029020_00626.sed --> Name = SR-6500_SN2029020_00626).


We can :
        > Read headers from one file with the funtion "Read_Header"                                                 : df = Obj.Read_Header()
        > Read headers from more files in one DataFrame With the function "Read_Headers"                            : df = Obj.Read_Headers()
            We can leave the argument "Name" empty as folows:  Name = " "
        > Read spectrum from one file with the funtion "Read_spectrum"                                              : df = Obj.Read_spectrum()
        > Read spectrums from more files in one DataFrame With the function "Read_spectrums"                        : df = Obj.Read_spectrums()
            we can leave argument "Name" empty as folows:  Name = " "
        > Save as .CSV, after having collected the data in "df" we can save them under a given name 
            "name = "DataFrame""  with the following command :                                                      : Obj.Save_as_csv(df , name = "DataFrame")


NOTE : 
        * The folder must containe only the files.
        * Please move the .csv file generated by "Obj.Save_as_csv" elsewhere and delete it from the current folder.
'''

class VNIR_SWIR(SpectraPreProcessing):

    def __init__(self, AdressFolder, Name):
        SpectraPreProcessing.__init__(self,AdressFolder)
        self.Name = Name

    def NameSpectrumColumns(self):
        '''
        Returns List of tuples containing the names of each column
        
        Note : you can change the folowing argument "ColomnsName" for naming the columns.
        '''
        ColomnsName = ["Wavelength", "Reflection %"]
        Name = [self.NameColumn(SampleName = self.Name, ColomnName = ["_",w]) for w in ColomnsName]   
        return Name

    def Header_to_Dict(self,NumberLine):
        ''' 
        Return the header lines as a dictionary 
        '''
        inputfile = open(self.FilePath(self.Name), 'r')
        Liste = list()
        for i in range(NumberLine):
            inputstr=inputfile.readline()
            inputspl=re.split("=",inputstr)
            Word = inputspl[0].rstrip()
            pos = Word.find(":")
            Liste.append(dict({Word[None:pos] : Word[pos+1 ::] }))
        inputfile.close()
        return Liste

    def Read_Header(self):
        ''' 
        Converts the header lines in the file to data frame

        Note : In VNIR_SWIR case the header lines are the lines before the word "Data:"
        '''
        global df
        try :
            List = [self.Dict_to_Df(Element) for Element in self.Header_to_Dict(self.FindWord("Data:",self.Name)+1)]
            # Add columns for the name : the name is also the name of the file "name.esp"
            df = self.Add_columns(List[0], "Sample", self.Name)
            # Join the laste two data frame in one data frame:
            for i in range(len(List)-1):
                df = self.Join_df(df , List[i+1])
        except IndexError:
            print("Please check that your file contains headers")
            df = pd.DataFrame({'None' : [np.nan]})
        return df

    def Read_Headers(self):
        ''' 
        Returns DataFrame containing  the header lines in all file exising in the folder 

        Note : this function concatenates all header lines from one or more files in the folder into one dataframe using Header_to_Df
        '''
        df = pd.DataFrame()
        li = self.NameFiles()
        for i in range(len(li)):
            V_S = VNIR_SWIR(self.AdressFolder, li[i]) 
            DF = V_S.Read_Header()
            df = df.append(DF, ignore_index = True) 
        return df

    

    def Read_spectrum(self):
        '''
        Returns DataFrame containing Spectrum
        
        Note :  > The columns name are multi level from the above function  "NameSpectrumColumns"
                > This function reads the spectrum when headers exist or not.
        '''
        File = self.FilePath(self.Name)
        Sep = self.Separator(Extension = self.FileExtension(self.Name))
        ColumnsName = self.NameSpectrumColumns()
        df = pd.read_table(File, header = self.FindWord("Data:", self.Name)+1, sep = Sep, names = ColumnsName) 
        return df 

    def Read_spectrums(self):
        ''' 
        Return DataFrame containing all spectrums in the folder
        '''
        Names = self.NameFiles()
        DF = [VNIR_SWIR(self.AdressFolder, Names[i]).Read_spectrum() for i in range(len(Names))]
        df = pd.DataFrame({("_","_","Wavelength"):DF[0][DF[0].columns[0]]})
        for i in range(len(DF)):
            df = df.join(DF[i][DF[i].columns[1::]])
        return df
    