# -*- coding: utf-8 -*-
from pkgs.SpectraPreProcessing import *
import pandas as pd
import json
import numpy as np

'''
Once the object is built :              Obj = Raman(AdressFolder, Name)

Where :
        > AdressFolder : The path to the folder containing the files.
        > Name : the file name without the extension (ex :  MesureR_2019 07 16_13h 49mn 38s L2C53.esp --> Name = MesureR_2019 07 16_13h 49mn 38s L2C53).


We can :
        > Read headers from one file with the funtion "Read_Header"                                                 : df = Obj.Read_Header()
        > Read headers from more files in one DataFrame With the function "Read_Headers"                            : df = Obj.Read_Headers()
            We can leave the argument "Name" empty as folows:  Name = " "
        > Read spectrum from one file with the funtion "Read_spectrum"                                              : df = Obj.Read_spectrum()
        > Read spectrums from more files in one DataFrame With the function "Read_spectrums"                        : df = Obj.Read_spectrums()
            we can leave argument "Name" empty as folows:  Name = " "
        > Save as .CSV, after having collected the data in "df" we can save them under a given name 
            "name = "DataFrame" "  with the following command :                                                      : Obj.Save_as_csv(df , name = "DataFrame")


NOTE : 
        * The folder must containe only the files.
        * The functions ended by "_" (example : Obj.Read_spectrum_()) used for extructing the integer portion from the NumberWaves.
        * Please move the .csv file generated by "Obj.Save_as_csv" elsewhere and delete it from the current folder.
'''


class Raman(SpectraPreProcessing):

    def __init__(self, AdressFolder, Name):
        SpectraPreProcessing.__init__(self,AdressFolder)
        self.Name = Name
    
    def NameSpectrumColumns(self):
        '''
        Returns List of tuples containing the names of each column
        
        Note : you can change the folowing argument "ColomnsName" for naming the columns.
        '''
        ColomnsName = ["NumberWaves", "Intensity"]
        Name = [self.NameColumn(SampleName = self.Name, ColomnName = [w]) for w in ColomnsName]   
        return Name


    def Header_to_Dict(self,NumberLine):
        ''' 
        Returns the header lines as a dictionary 
        '''
        inputfile = open(self.FilePath(self.Name), 'r')
        Liste = list()
        for i in range(NumberLine):
            inputstr=inputfile.readline()
            inputspl=re.split("=",inputstr)
            Liste.append(json.loads(inputspl[1]))
        inputfile.close()
        return Liste

    def Read_Header(self):
        ''' 
        Convertes the header lines in the file to data frame

        Note : In this case the header lines are recognized by the hashtags "#" : #exp_cfg and #proc_cfg
        '''
        global df
        try :
            List = [self.Dict_to_Df(Element) for Element in self.Header_to_Dict(self.Count_Hachtags(self.Name))]
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

        Note : this function concatenates all header lines from one or more filesin  the folder into one dataframe using Header_to_Df
        '''
        df = pd.DataFrame()
        li = self.NameFiles()
        for i in range(len(li)):
            Rmn = Raman(self.AdressFolder, li[i]) 
            DF = Rmn.Read_Header()
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
        Names = self.NameSpectrumColumns()
        if self.Count_Hachtags(self.Name) == 0 :
            df = pd.read_table(File, header = None, sep = Sep, names = Names)
        else:
            df = pd.read_table(File, header = self.Count_Hachtags(self.Name) , sep = Sep ) 
            df2 = pd.DataFrame(data= {Names[i]: [np.float32(df.columns.to_list()[i])] for i in range(len(df.columns))})
            df = df.rename(columns = {df.columns[i] : Names[i] for i in range(len(df.columns))})
            df = df2.append(df, ignore_index = True) 
        return df 

    def Read_spectrums(self):
        ''' 
        Return DataFrame containing all spectrums in the folder
        '''
        Names = self.NameFiles()
        # Reading all spectrums and collecte them in list :
        DF_ = [Raman(self.AdressFolder, Names[i]).Read_spectrum() for i in range(len(Names))]
        # Collecting the names of spectrums in list :
        ListOfNameAllSpec = [Raman(self.AdressFolder, Names[i]).NameSpectrumColumns() for i in range(len(Names))]
        # Builting the Data Frame Contining All X_values :
        DF = self.X_DataFrame(DF_, "NumberWaves" )
        # Loop in all Data frame in DF_ :
        for i in range(len(DF_)):
            Index_df_in_DF = [self.FindIndex(DF,DF_[i][DF_[i].columns[0]][j]) for j in range(len(DF_[i]))]
            df = pd.DataFrame(DF_[i].values, index = Index_df_in_DF)
            df.columns=pd.MultiIndex.from_tuples(ListOfNameAllSpec[i])
            DF = DF.join(df[df.columns[1::]])
        return DF
    
    def Read_Interpolated_spectrums(self):
        ''' '''
        df = self.Read_spectrums()
        df = df.interpolate(method='linear')
        for k in range(len(df.columns)):
            First_NotNAN_value = df[df.columns[k]].loc[df[df.columns[k]].first_valid_index()]
            Last_NotNAN_value = df[df.columns[k]].loc[df[df.columns[k]].last_valid_index()]
            for i in range(df[df.columns[k]].first_valid_index()):
                df[df.columns[k]].loc[i] = First_NotNAN_value
            for i in range(df[df.columns[k]].last_valid_index(), len(df[df.columns[k]]), 1):
                df[df.columns[k]].loc[i] = Last_NotNAN_value

        return df 

    def Read_spectrum_(self):
        '''
        Returns DataFrame containing Spectrum, keeping only the integer portion of NumberWaves
        
        Note :  > The columns name are multi level from the above function  "NameSpectrumColumns"
                > This function reads the spectrum when headers exist or not.
        '''
        File = self.FilePath(self.Name)
        Sep = self.Separator(Extension = self.FileExtension(self.Name))
        Names = self.NameSpectrumColumns()
        if self.Count_Hachtags(self.Name) == 0 :
            df = pd.read_table(File, header = None, sep = Sep, names = Names)
            df[df.columns[0]] = df[df.columns[0]].astype(int)
        else:
            df = pd.read_table(File, header = self.Count_Hachtags(self.Name) , sep = Sep ) 
            df2 = pd.DataFrame(data= {Names[i]: [np.float32(df.columns.to_list()[i])] for i in range(len(df.columns))})
            df = df.rename(columns = {df.columns[i] : Names[i] for i in range(len(df.columns))})
            df = df2.append(df, ignore_index = True) 
            df[df.columns[0]] = df[df.columns[0]].astype(int)
        return df 

    def Read_spectrums_(self):
        ''' 
        Return DataFrame containing all spectrums in the folder
        '''
        Names = self.NameFiles()
        # Reading all spectrums and collecte them in list :
        DF_ = [Raman(self.AdressFolder, Names[i]).Read_spectrum_() for i in range(len(Names))]
        # Collecting the names of spectrums in list :
        ListOfNameAllSpec = [Raman(self.AdressFolder, Names[i]).NameSpectrumColumns() for i in range(len(Names))]
        # Builting the Data Frame Contining All X_values :
        DF = self.X_DataFrame(DF_, ("_", "NumberWaves") )
        # Loop in all Data frame in DF_ :
        for i in range(len(DF_)):
            Index_df_in_DF = [self.FindIndex(DF,DF_[i][DF_[i].columns[0]][j]) for j in range(len(DF_[i]))]
            df = pd.DataFrame(DF_[i].values, index = Index_df_in_DF)
            df.columns=pd.MultiIndex.from_tuples(ListOfNameAllSpec[i])
            DF = DF.join(df[df.columns[1::]])
        return DF
    
    def Read_Interpolated_spectrums_(self):
        ''' '''
        df = self.Read_spectrums_()
        df = df.interpolate(method='linear')
        for k in range(len(df.columns)):
            First_NotNAN_value = df[df.columns[k]].loc[df[df.columns[k]].first_valid_index()]
            Last_NotNAN_value = df[df.columns[k]].loc[df[df.columns[k]].last_valid_index()]
            for i in range(df[df.columns[k]].first_valid_index()):
                df[df.columns[k]].loc[i] = First_NotNAN_value
            for i in range(df[df.columns[k]].last_valid_index(), len(df[df.columns[k]]), 1):
                df[df.columns[k]].loc[i] = Last_NotNAN_value
        return df 



