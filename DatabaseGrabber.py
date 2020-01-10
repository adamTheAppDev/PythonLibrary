# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:37:08 2017

@author: AmatVictoriaCuramIII
"""

#This is a database management/query tool 

def DatabaseGrabber(ticker):    
    import pandas as pd
    dataframe = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\' + 
                  ticker + '\\' + ticker)
    for i in dataframe.columns:
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    return dataframe
