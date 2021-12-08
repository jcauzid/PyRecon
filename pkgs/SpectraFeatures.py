# -*- coding: utf-8 -*-
import re
import os
import numpy as np
import pandas as pd
import spectral.io.envi as envi
import pysptools.spectro as spectro
from pkgs.SpectraPreProcessing import *

import shutil


class SpectraFeatures(object):  
    
    def __init__(self, AdressFolder, SpecDataFrame, Name, LowValue = None, HighValue = None, startContinuum=None, stopContinuum=None, normalize=False, Scale = False, NumberShift = 2, Verbose = False):
        """ 
        AdressFolder_hdr     = "Path" where saving the hdr file.
        SpecDataFrame        = "DataFrame" The data "intensity"
        Name_SPC             = "Str" The name of the samples 
        """
        self.startContinuum             = startContinuum   
        self.stopContinuum              = stopContinuum
        self.LowValue                   = LowValue
        self.HighValue                  = HighValue
        self.normalize                  = normalize
        self.Scale                      = Scale
        self.NumberShift                = NumberShift
        self.AdressFolder               = AdressFolder
        self.SpecDataFrame              = SpecDataFrame  
        self.Name                       = Name
        self.samples                    = 1
        self.bands                      = 1
        self.ObjProcess                 = SpectraPreProcessing(AdressFolder = self.AdressFolder)
        self.Verbose                    = Verbose

        self.path, self.path_Region     = self.ResutPath()

    def Processing_Spectra(self):

        obj = self.ObjProcess
        DF = obj.ExtractRegion(DataFrame = self.SpecDataFrame, LowValue = self.LowValue, HighValue = self.HighValue) 
        if self.Scale is False :
            pass
        else : 
            DF = obj.SpecScale(DataFrame = DF, NumberShift = self.NumberShift)
        
        DF_    = DF[DF.columns[1]].to_frame().T.to_numpy()
        lines  = np.shape(DF_)[1]
        wvl    = {val for val in DF[DF.columns[0]].values}

        return lines, wvl, DF, DF_  

    def Header_HSI(self): 
        """ 
        
        """
        lines, wvl, DF, DF_  = self.Processing_Spectra()
        hdr = {
        "description"                           :        " Messing Info ",
        "spectra names"                         :            ["spectra"],
        "samples"                               :            self.samples,
        "lines"                                 :            lines,
        "bands"                                 :            self.bands,
        "header offset"                         :                0,
        "file type"                             :         "ENVI Standard",
        "data type"                             :               12,
        "interleave"                            :             "bsq",
        "sensor type"                           :        " Messing Info ",
        "byte order"                            :                0,
        "map info"                              :        " Messing Info ",
        "coordinate system string"              :        " Messing Info ",
        "wavelength units"                      :        " Messing Info ",
        "band names"                            :        " Messing Info ",
        "wavelength"                            :             wvl
        }

        return hdr

    

    def HSI(self):
        """
            DATA : the WVL/NWV dataframe
        """

        path, path_Region = self.ResutPath()
        lines, wvl, DF, DF_  = self.Processing_Spectra()

        hdr = self.Header_HSI()
        img = envi.SpectralLibrary(data = DF_ , header  = hdr) 
        img.save(path_Region + os.path.sep + "spectra" )

    
        rd = spectro.EnviReader(path_Region + os.path.sep + "spectra.hdr")
        
        lib = spectro.USGS06SpecLib(rd) 
        WVE = lib.get_wvl()
        spc = lib.spectra

        return lib, WVE, spc


    
    def SpectrumConvexHullQuotient(self):
        """

        """
        lib, WVE, spc = self.HSI()

        for spectrum, mineral, sample_id, descrip, idx in lib.get_next():
            schq = spectro.SpectrumConvexHullQuotient(spectrum=spectrum,wvl=WVE, normalize= self.normalize)
            #plot_name = '{0}_{1}_{2}'.format(idx, mineral, sample_id) 
            plot_name = '{0}_{1}'.format(idx, self.Name)
        return schq, plot_name
    
    def FeaturesConvexHullQuotient(self, substance = "Spectr" ,baseline = 1):
        """
        
        """
        lib, WVE, spc = self.HSI()

        for spectrum, sample_id, descrip, idx in lib.get_substance(substance = substance, sample = None ):
            fea = spectro.FeaturesConvexHullQuotient(spectrum, WVE, baseline = baseline , startContinuum = self.startContinuum , stopContinuum = self.stopContinuum , normalize = self.normalize )
            #plot_name = '{0}_{1}'.format(substance , sample_id )
            plot_name = self.Name
            if self.Verbose is True : 
                fea.print_stats('all')
                #self.Plot_Features(baseline = baseline)
        return fea, plot_name
    
    def Features(self, substance = "Spectr" ,baseline = 1):
        """

        """
        path, path_Region = self.ResutPath()
        lines, wvl, DF, DF_  = self.Processing_Spectra() 

        schq , _  =self.SpectrumConvexHullQuotient()
        fea , _  = self.FeaturesConvexHullQuotient(substance ,baseline)

        NumPeaks = fea.get_number_of_kept_features()
        peaks = list()
        if NumPeaks == 0 : 
            peaks.append({
                          'Peak position'      : 00.00,
                          'Peak value'         : 00.00,
                          'Depth'              : 00.00, 
                          'FWHM'               : 00.00,
                          'Area '              : 00.00
                        })
        else :
            for i in range(1,NumPeaks+1,1):
                idx = self.ObjProcess.FindIndex(XDataFrame = DF ,ValuesToCollect = fea.get_absorbtion_wavelength(i)) 
                peaks.append({
                            'Peak position'      : fea.get_absorbtion_wavelength(i),
                            'Peak value'         : self.SpecDataFrame[self.SpecDataFrame.columns[1]][idx], 
                            'Depth'              : fea.get_absorbtion_depth(i), 
                            'FWHM'               : fea.get_full_width_at_half_maximum(i),
                            'Area '              : fea.get_area(i)
                            })
                
        df_Result = pd.DataFrame(data=peaks)
        df_Result.to_csv(path_Region + os.path.sep + '{} Peaks : ROI [{} to {}], Normalization [{}].csv'.format(self.Name, self.startContinuum, self.stopContinuum, self.normalize)) 

        d_HP = {'HullPoint_X': schq.hx, 'HullPoint_Y': schq.hy}
        df_HP = pd.DataFrame(data=d_HP)
        df_HP.to_csv(path_Region + os.path.sep + '{} Hull Points : Normalization [{}].csv'.format(self.Name ,self.normalize))

        self.removeTmp(path = path , path_Region = path_Region ) 

        return df_Result, df_HP

    def Plot_Features(self, substance = "Spectr" ,baseline = 1): 
        """

        """
        path, path_Region = self.ResutPath()
        
        # SpectrumConvexHullQuotient
        schq, plot_name     = self.SpectrumConvexHullQuotient()
        schq.plot(path_Region, plot_name)

        # FeaturesConvexHullQuotient :
        fea , plot_name     = self.FeaturesConvexHullQuotient(substance ,baseline)
        fea.plot_convex_hull_quotient(path_Region , plot_name)
        fea.plot(path_Region , plot_name, feature='all')

        self.removeTmp(path = path , path_Region = path_Region )
    
    def ResutPath(self):
        """

        """
        PATH = self.AdressFolder + os.path.sep + "Results"
        path = PATH + os.path.sep + self.Name
        path_Region = path + os.path.sep + 'ROI [{} to {}], Normalize [{}]'.format(self.startContinuum,self.stopContinuum,self.normalize)
        try:
            os.mkdir(PATH, mode = 0o777)
        except FileExistsError:
            pass
        try:
            os.mkdir(path, mode = 0o777)
        except FileExistsError:
            pass
        finally :
            obj = self.ObjProcess
            shutil.copy(obj.FilePath(self.Name), path + os.path.sep + "spectra" + obj.FileExtension(self.Name) )
        try:
            os.mkdir(path_Region, mode = 0o777)
        except FileExistsError:
            pass
        return path, path_Region


    def removeTmp(self,path,path_Region):
        try:
            os.remove(path_Region + os.path.sep + "spectra.hdr")
            os.remove(path_Region + os.path.sep + "spectra.sli")
            os.remove(path + os.path.sep + "spectra.csv")
        except OSError as e:
            pass