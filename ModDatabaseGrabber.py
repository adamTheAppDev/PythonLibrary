# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a modified version of DatabaseGrabber - a query tool

#Define fucntion
def ModDatabaseGrabber(ticker):    
    #Import modules
    import pandas as pd 
    #It will be neccessary for you to change the location of the working directory
    #in order to load the data into the model. Please modify to match the destination 
    #of the working directory folder
    #Read in data
    dataframe = pd.read_pickle('F:\\Users\\Username\\DirectoryLocation\\PriceHistory\\' + 
                  ticker)
    #For all column's values
    for i in dataframe.columns:
        #Change data type to numeric
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    #Delete duplicate columns + rows
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    #Output table
    return dataframe
