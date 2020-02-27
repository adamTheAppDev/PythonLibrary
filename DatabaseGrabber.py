# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a directory management/query tool 

#Define function 
def DatabaseGrabber(ticker):    
    #Import modules
    import pandas as pd
    
    #Assign dataframe by reading pickle 
    dataframe = pd.read_pickle('F:\\Users\\UserName\\DirectoryLocation\\' + 
                  ticker + '\\' + ticker)
    
    #For all columns in dataframe
    for i in dataframe.columns:
        #Make numeric datatype
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    #Erase duplicate columns
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    #Erase duplicate rows
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    #Output dataframe
    return dataframe
