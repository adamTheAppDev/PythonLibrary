# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:41:00 2019

@author: AmatVictoriaCuramIII
"""

#Yahoo Daily Grabber
def YahooSourceDailyGrabber(ticker):    
    import pandas as pd
    dataframe = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\' +
            'YahooSource\\ProcessedData\\' + 'DAY' + '\\' + 'DAY-' + ticker + '\\' + 'DAY-' + ticker)
    for i in dataframe.columns:
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    return dataframe