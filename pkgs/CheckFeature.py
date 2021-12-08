# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from collections import Counter

from itertools import product
import os

from pkgs.SpectraFeatures import *
from pkgs.SpectraPreProcessing import *
from pkgs.Raman import *
from pkgs.IR import *
from pkgs.LIBS import *
from pkgs.VNIR_SWIR import *
from pkgs.XRF import *

class CheckFeature(object):  
    
    def __init__(self,Tool ,AdressFolder, SpecDataFrame, Name, DecisionTree , LowValue = None, HighValue = None, startContinuum=None, stopContinuum=None, normalize=False, Scale = False, NumberShift = 2, Verbose = False):
        """ 


        """
        self.Tool                       = Tool
        self.startContinuum             = startContinuum   
        self.stopContinuum              = stopContinuum
        self.LowValue                   = LowValue
        self.HighValue                  = HighValue
        self.normalize                  = normalize
        self.Scale                      = Scale
        self.NumberShift                = NumberShift
        self.AdressFolder               = AdressFolder
        self.DecisionTree               = DecisionTree
        self.SpecDataFrame              = SpecDataFrame  
        self.Name                       = Name
        self.Verbose                    = Verbose

    def Peaks(self):
        """
        

        """
        results =  pd.DataFrame() 
        for i in range(len(self.startContinuum)):
            OBJ = SpectraFeatures( self.AdressFolder, self.SpecDataFrame, self.Name, LowValue =  self.LowValue, HighValue = self.HighValue,
                                    startContinuum = self.startContinuum[i], stopContinuum = self.stopContinuum[i], normalize = self.normalize, Scale = self.Scale, NumberShift = self.NumberShift, Verbose = self.Verbose)
            df_peak, df_HP = OBJ.Features(baseline = 1)
            OBJ.Plot_Features(baseline = 1)
            results = results.append(df_peak)

        NANpeak = [{
                'Peak position'      : 00,
                'Peak value'         : 00, 
                'Depth'              : 00, 
                'FWHM'               : 00,
                'Area '              : 00
            }]

        df_NANpeak = pd.DataFrame(data=NANpeak) 
        results = results.append(df_NANpeak) 

        results.index = np.arange(len(results))

        try:
            os.remove(OBJ.path + os.path.sep + "spectra.txt")
        except OSError as e:
            pass

        results = [results.iloc[results.index == i].to_dict(orient = 'records') for i in results.index]

        return results, OBJ

    def idx_Region_(self, DF_Region, Feature) : 
        """


        """
        Feature = Feature[0]
        peak_position = Feature['Peak position']
        index = DF_Region.index
        idx = []
        condition = (DF_Region[DF_Region.columns[0]] <= peak_position) & (DF_Region[DF_Region.columns[1]] >= peak_position)
        indices = index[condition]
        idx = indices.tolist()   
        Feature['Index in decision tree'] = idx
        Feature['Score'] = 0
        return Feature
    
    def idx_DT_(self, Feature):
        """


        """
        Liste_Features = []
        idx__ = []
        for j in range(4,len(self.DecisionTree.columns), 2):
            Feature_ = self.idx_Region_( DF_Region = self.DecisionTree[self.DecisionTree.columns[j:j+2]], Feature = Feature) 
            Liste_Features.append(Feature_['Index in decision tree'])
            idx__ += Feature_['Index in decision tree']
        Feature_["idx"] = idx__
        Feature_['Index in decision tree'] = Liste_Features
        return Feature_


    def idx_Mineral_(self, PeakPoints):
        """


        """
        
        INDEX = []
        Dict_Features = []
        for i in range(len(PeakPoints)):
            Feature_ = self.idx_DT_(Feature = PeakPoints[i])
            Dict_Features.append(Feature_)
            INDEX.append(Feature_['Index in decision tree'])
        mat = np.asarray(INDEX, dtype=object) 
        try :
            m, n, _ = np.shape(mat)
        except ValueError :
            m, n = np.shape(mat)
        indices = [np.sum(mat[:,i]) for i in range(n) ]
        return indices, Dict_Features

    def Check_indices_Validity(self, indices, NumberRegions = 3):
        """


        """
        for i in range(NumberRegions):
            if (len(indices[i]) == 00) :
                return False
            else :
                return True 
        
    def DataFrame_Features(self, PeakPoints):
        """
        

        """
        
        indices, Dict_Features = self.idx_Mineral_(PeakPoints = PeakPoints)
        data = [{'Peak position'                            : 00,
                'Peak value'                                : 00, 
                'Depth'                                     : 00, 
                'FWHM'                                      : 00, 
                'Area '                                     : 00, 
                'Score'                                     : 00, 
                'idx'                                       : [np.nan], 
                '{}_Region'.format(self.Tool )              : [np.nan], }]
        
        DataFrame = pd.DataFrame(data = data)
        if self.Check_indices_Validity(indices):
            Dict_Features_filtred = [] 
            indices_filtred = list(filter(None, indices))
            intersection  = Counter(indices_filtred[0])

            for i in range(0,len(indices_filtred)):
                intersection = intersection & Counter(indices_filtred[i])
            if not (len(list(intersection.keys())) == 0) :
                List_comon_idx = list(intersection.keys())
                for point in Dict_Features:
                    num = 1
                    list2 = point["Index in decision tree"]
                    numRlist = []
                    for i in range(len(list2)):
                        if any(item in list2[i] for item in List_comon_idx):
                            numRlist.append(num)
                            point['Score'] = point['Peak value']
                            Dict_Features_filtred.append(point)
                        num += 1
                    
                    point['{}_Region'.format(self.Tool)] = numRlist
                    
                for point in Dict_Features_filtred:
                    ip = Counter(point['idx']) & Counter(List_comon_idx) 
                    point["idx"] = list(ip.keys())
                
                result = pd.DataFrame()
                for point in Dict_Features_filtred:
                    result = result.append(pd.DataFrame([point]))
                result.index = np.arange(len(result))
                result = result.drop_duplicates(subset=['Peak position'])
                result = result.drop(["Index in decision tree"], axis=1)

                DF = pd.DataFrame()
                for j in range(len(List_comon_idx)):
                    DF_ = pd.DataFrame(columns = result.columns)
                    for i in range(len(result)):
                        df_ = result.iloc[i]
                        if List_comon_idx[j] in df_["idx"]:
                            DF_ = DF_.append(df_, sort=False)
                            DF_["idx"] = List_comon_idx[j]
                    DF = DF.append(DF_, sort=False)
                DF.index = np.arange(len(DF))
                result = DF 
            else : 
                    result = DataFrame
        else : 
            result = DataFrame
        
        return result
    def PeaksDataFrame(self, PeakPoints, TolRegion = 2):
        """
        
        
        """
        df_Dict_Features_filtred = self.DataFrame_Features(PeakPoints = PeakPoints)
        EmptyheaderArrays = [
                np.array(["{}_Region {}".format(self.Tool ,1)]*6 + ["{}_Region {}".format(self.Tool ,2)]*6 + ["{}_Region {}".format(self.Tool ,3)]*6),
                np.array(list(df_Dict_Features_filtred.columns[0:6])*3)
             ]
        Emptydata = np.array([[None]* 18]) 
        EmptyResult = pd.DataFrame(data = Emptydata, columns = EmptyheaderArrays)
        Emptytupleindexes_ = [(
                                self.Name,
                                None, 
                                self.Tool,
                                None,
                                None,
                                None)] 
        EmptyResult.index = pd.MultiIndex.from_tuples(Emptytupleindexes_, names=["Sample","Score","Tool","Groupe","Subgoupe","Mineral"])
        Results = pd.DataFrame() 
        
        if not isinstance(df_Dict_Features_filtred["idx"].values[0], list) :
            headerArrays = [
                np.array(["{}_Region {}".format(self.Tool ,1)]*6 + ["{}_Region {}".format(self.Tool ,2)]*6 + ["{}_Region {}".format(self.Tool ,3)]*6),
                np.array(list(df_Dict_Features_filtred.columns[0:6])*3)
            ]
            data = np.array([[0.0]* 18]) 
            dataframe = pd.DataFrame(data = data, columns = headerArrays)
            tupleindexes_ = [(
                                None,
                                None, 
                                None,
                                None,
                                None,
                                None)] 
            dataframe.index = pd.MultiIndex.from_tuples(tupleindexes_, names=["Sample","Score","Tool","Groupe","Subgoupe","Mineral"])
            DF = pd.DataFrame()
            for i in range(len(df_Dict_Features_filtred)):
                df_ = df_Dict_Features_filtred.iloc[i]
                for k in df_["{}_Region".format(self.Tool)]:
                    headerlocalArrays = [
                        np.array(["{}_Region {}".format(self.Tool ,k)]*6),
                        np.array(list(df_Dict_Features_filtred.columns[0:6]))
                    ]
                    df__ = pd.DataFrame(data = np.array([df_[0:6].values]), columns = headerlocalArrays)
                    tupleindexeslocal = [(self.Name,None,self.Tool,
                                    self.DecisionTree[self.DecisionTree.columns[1]][df_['idx']],
                                    self.DecisionTree[self.DecisionTree.columns[2]][df_['idx']],
                                    self.DecisionTree[self.DecisionTree.columns[3]][df_['idx']])]
                    df__.index = pd.MultiIndex.from_tuples(tupleindexeslocal, names=["Sample","Score","Tool","Groupe","Subgoupe","Mineral"])
                    dataframe = dataframe.iloc[1: , :]
                    dataframe = dataframe.append(df__, sort = False)
                DF = DF.append(dataframe, sort = False)
            
            #Groupping Minerals :
            Minerals = DF.index
            Minerals = Minerals.drop_duplicates(keep='first')
            for k in range(len(Minerals)):
                MineralDataFrame = DF.xs(Minerals[k])
                list_DFF_ = list()
                Scores = []
                for j in range(3):
                    DF_ = MineralDataFrame[MineralDataFrame.columns[j*6:(j*6 + 6)]]
                    DF_ = DF_.dropna(axis=0)
                    if not DF_.empty:
                        Scores_ = [score[0] for score in  DF_.iloc[:, DF_.columns.get_level_values(1)=='Score'].values]
                        Scores.append(max(Scores_))
                        list_DFF_.append(DF_) 
                DFF_ = list_DFF_[0]
                if not DFF_.empty:
                    for h in range(1,len(list_DFF_)):
                        DFF_ = DFF_.merge(list_DFF_[h],how='inner' ,on = list_DFF_[0].index.names)
                    if len(Scores) >= TolRegion:
                        y = list(Minerals[k])
                        y[1] = np.sum(Scores)
                        Mineral = tuple(y)
                        DFF_.index = pd.MultiIndex.from_tuples([Mineral]*len(DFF_) ,names=DFF_.index.names)
                        Results = Results.append(DFF_)
                    else :
                        Results = EmptyResult
                else : 
                    Results = EmptyResult
        else : 
            Results = EmptyResult

        return Results

