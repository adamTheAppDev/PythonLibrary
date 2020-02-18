# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a database management/query tool 

def DatabaseGrabber(ticker):    
    import pandas as pd
    dataframe = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' + 
                  ticker + '\\' + ticker)
    for i in dataframe.columns:
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    return dataframe
