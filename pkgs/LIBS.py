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
from pkgs.SpectraPreProcessing import *
import pandas as pd


'''
Once the object is built :              Obj = LIBS(AdressFolder, Name)

Where :
        > AdressFolder : The path to the folder containing the files.
        > Name : the file name without the extension (ex : 22-1_20201022_113302_AM_AverageSpectrum.csv --> Name = 22-1_20201022_113302_AM_AverageSpectrum).


We can :
        > Read spectrum from one file with the funtion "Read_spectrum"                                              : df = Obj.Read_spectrum()
        > Read spectrums from more files in one DataFrame With the function "Read_spectrums"                        : df = Obj.Read_spectrums()
            we can leave the argument "Name" empty as folows:  Name = " "
        > Save as .CSV, after having collected the data in "df" we can save them under a given name 
            "name = "DataFrame""  with the following command :                                                      : Obj.Save_as_csv(df , name = "DataFrame")


NOTE : 
        * The folder must containe only the files.
        * Please move the .csv file generated by "Obj.Save_as_csv" elsewhere and delete it from the current folder.
'''

class LIBS(SpectraPreProcessing):

    def __init__(self, AdressFolder, Name):
        SpectraPreProcessing.__init__(self,AdressFolder)
        self.Name = Name

    def NameSpectrumColumns(self):
        '''
        Returns List of tuples containing the names of each column
        
        Note : you can change the folowing argument "ColomnsName" for naming the columns.
        '''
        ColomnsName = ["Wavelength", "Intensity"]
        Name = [self.NameColumn(SampleName = self.Name, ColomnName = ["_",w]) for w in ColomnsName]   
        return Name

    def Read_spectrum(self):
        '''
        Returns DataFrame containing Spectrum
        
        Note :  > The columns name are multi level from the above function  "NameSpectrumColumns"
                > This function reads the spectrum when headers exist or not.
        '''
        File = self.FilePath(self.Name)
        Sep = self.Separator(Extension = self.FileExtension(self.Name))
        Names = self.NameSpectrumColumns()
        df = pd.read_csv(File, header = 0, sep = Sep, names = Names) 
        return df 

    def Read_spectrums(self):
        '''' 
        Return DataFrame containing all spectrums in the folder
        '''
        Names = self.NameFiles()
        DF = [LIBS(self.AdressFolder, Names[i]).Read_spectrum() for i in range(len(Names))]
        df = pd.DataFrame({("_","_","Wavelength"):DF[0][DF[0].columns[0]]})
        for i in range(len(DF)):
            df = df.join(DF[i][DF[i].columns[1::]])
        return df
    
