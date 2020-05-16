# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a local database query tool

#Define function
def YahooSourceDailyGrabber(ticker):    
    #Import modules
    import pandas as pd
    dataframe = pd.read_pickle('Z:\\Users\\Username\\DirectoryLocation\\DataSources\\' +
            'YahooSource\\ProcessedData\\' + 'DAY' + '\\' + 'DAY-' + ticker + '\\' + 'DAY-' + ticker)
    #Make all columns numeric data type
    for i in dataframe.columns:
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    #Delete duplicate rows and columns    
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    #Ouput
    return dataframe
