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
import os
import numpy as np
import pandas as pd
from PyRecon import *
from pkgs.ReconciliationMatrix import *
from pkgs.Raman import *

class ElementaryQuantyficationProportion(object): 

    def __init__(self, AdressFolder = 'None', nameSpectra = 'None', AdressRefFolder = 'None', AdressDensitisFolder = 'None', AdressCompositionFolder = 'None', valinf = 'None', valsup = 'None' ):
        """
        
        """
        self.AdressRefFolder            = AdressRefFolder
        self.AdressFolder               = AdressFolder
        self.AdressDensitisFolder       = AdressDensitisFolder
        self.AdressCompositionFolder    = AdressCompositionFolder
        self.nameSpectra                = nameSpectra
        self.valinf                     = valinf
        self.valsup                     = valsup
        self.nameElemnt                 = ["Cal_1_","Ank_1","Dol_1","Sd_3","Mgs_1"]


    def VectorExtruction(self, AdressFolder, name, valinf, valsup):
        """
        
        """
        obj = Raman(AdressFolder= AdressFolder,Name= name)
        DF_Ref  = obj.Read_spectrum()
        idx     = DF_Ref.index
        vector = []
        vector_unscaled = []
        for j in range(len(valinf)):
            Condi   =  (DF_Ref[DF_Ref.columns[0]].astype(int) <= valsup[j]) & (DF_Ref[DF_Ref.columns[0]].astype(int) >= valinf[j])
            indices = idx[Condi].tolist()
            valu = DF_Ref[DF_Ref.columns[1]][indices].values
            vector_unscaled.append(max(valu))
            vector.append(np.sum(valu)/ len(valu))
        vector_scaled = [(i-min(vector))/(max(vector)-min(vector)) for i in vector]
        return vector_scaled, vector_unscaled 

    def MatrixRef(self, valinf, valsup):
        """

        """
        Matrix  = []
        for i in range(len(self.nameElemnt)):
            Vector, vector_unscaled  = self.VectorExtruction(AdressFolder = self.AdressRefFolder , name = self.nameElemnt[i], valinf = valinf, valsup = valsup)
            Matrix.append(Vector)
        Matrix = np.linalg.inv(np.array(Matrix))
        return Matrix

    def MineralMassProportion(self,valinf, valsup):
        """

        """
        Vector, vector_unscaled   = self.VectorExtruction(AdressFolder = self.AdressFolder , name = self.nameSpectra , valinf = valinf, valsup = valsup)
        Matrix = self.MatrixRef(valinf = valinf, valsup = valsup )
        Product = np.dot(Matrix, Vector)
        # Replace the negative values par zero :
        Product[Product < 0] = 0
        # Normlizing :
        VolumeResult = Product / np.sum(Product)
        # Impoting the densities : 
        densities = self.ReadVector(self.AdressDensitisFolder)
        # Caluculating the mass of each miniral :
        MineralsMass = [x*y for x, y in zip(VolumeResult,densities)] 
        # Miniral Mass Proportion :
        result = MineralsMass/ np.sum(MineralsMass)
        return result 
    
    def MassProportion(self):
        """
        
        """
        # Importing Compositions : 
        Cal = self.ReadVector(self.AdressCompositionFolder + os.path.sep + "Ref-cal-El-mass.csv")
        Ank = self.ReadVector(self.AdressCompositionFolder + os.path.sep + "Ref-ank-El-mass.csv")
        Dol = self.ReadVector(self.AdressCompositionFolder + os.path.sep + "Ref-dol-El-mass.csv")
        Sid = self.ReadVector(self.AdressCompositionFolder + os.path.sep + "Ref-sid-El-mass.csv")    
        Mgs = self.ReadVector(self.AdressCompositionFolder + os.path.sep + "Ref-mgs-El-mass.csv")
        
        # E matrix :
        GroupMinerals = [Cal, Ank, Dol, Sid, Mgs]
        GroupMinerals = [Mineral / np.sum(Mineral) for Mineral in GroupMinerals]
        E_Matrix = np.array(GroupMinerals)

        return E_Matrix

    def CarbonateElementaryProportion(self):

        MineralMassProportion   = self.MineralMassProportion(valinf = self.valinf, valsup = self.valsup ) 
        MassProportion          = self.MassProportion()
        result                  = np.dot( MineralMassProportion, MassProportion)
        result                  = result/ np.sum(result)


        data  = {
                "Mg" : result[3],
                "Al" : np.nan,
                "Si" : np.nan,
                "P"  : np.nan,
                "S"  : np.nan,
                "K"  : np.nan,
                "Ca" : result[2],
                "Ti" : np.nan,
                "Mn" : result[5],
                "Fe" : result[4],
                "Cu" : np.nan,
                "Zn" : np.nan,
                "Ba" : np.nan,
                "P"  : np.nan
            }
        columns = ["Mg","Al","Si","P","S","K","Ca","Ti","Mn","Fe","Cu","Zn","Ba","P"]
        Df = pd.DataFrame(data, columns = columns, index = ["CARBONATE"])
        
        return Df

    def ReadVector(self,adress):
        """
        
        """
        Vector = pd.read_csv(adress)
        Vector = Vector.columns.astype(float).to_numpy()

        return Vector
    
    def Chlorite_Raman(self,  x):

        # Raman :
        Fe    = -1.253567 * x + 856.332851
        Mg    =  0.785602 * x - 515.497816
        Si    =  0.225416 * x - 138.330722
        Al    = -0.194943 * x + 141.101313
        Fe_r  = -0.042263 * x + 28.910469

        data  = {
                "Mg" : Mg,
                "Al" : Al,
                "Si" : Si,
                "P"  : np.nan,
                "S"  : np.nan,
                "K"  : np.nan,
                "Ca" : np.nan,
                "Ti" : np.nan,
                "Mn" : np.nan,
                "Fe" : Fe,
                "Cu" : np.nan,
                "Zn" : np.nan,
                "Ba" : np.nan,
                "P"  : np.nan
            }
        columns = ["Mg","Al","Si","P","S","K","Ca","Ti","Mn","Fe","Cu","Zn","Ba","P"]
        Df = pd.DataFrame(data, columns = columns, index = ["CHLORITE"])
        return Df 
        
    def Chlorite_VNIR_SWIR(self,  x):
    
        # VNIR-SWIR : 
        Fe    =  1.433622 * x - 3216.572618
        Mg    = -1.014806 * x + 2298.884521
        Si    = -0.301479 * x + 691.850626
        Al    =  0.115474 * x - 250.030429
        Fe_r  =  0.047754 * x - 107.099162

        data  = {
                "Mg" : Mg,
                "Al" : Al,
                "Si" : Si,
                "P"  : np.nan,
                "S"  : np.nan,
                "K"  : np.nan,
                "Ca" : np.nan,
                "Ti" : np.nan,
                "Mn" : np.nan,
                "Fe" : Fe,
                "Cu" : np.nan,
                "Zn" : np.nan,
                "Ba" : np.nan,
                "P"  : np.nan
            }
        columns = ["Mg","Al","Si","P","S","K","Ca","Ti","Mn","Fe","Cu","Zn","Ba","P"]
        Df = pd.DataFrame(data, columns = columns, index = ["CHLORITE"])
        return Df 




    




 


    
    








