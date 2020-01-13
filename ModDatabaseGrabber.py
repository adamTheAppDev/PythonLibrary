# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:37:08 2017

@author: Adam Reinhold Von Fisher - adamrvfisher@gmail.com 
linkedin.com/in/adamrvfisher
"""

#This is a modified version of DatabaseGrabber - a query tool

def ModDatabaseGrabber(ticker):    
    import pandas as pd 
    #It will be neccessary for you to change the location of the working directory
    #in order to load the data into the model. Please modify line 13 to match the destination 
    #of the working directory folder
    dataframe = pd.read_pickle('F:\\Users\\Adam\\Desktop\\WorkingDirectory\\PriceHistory\\' + 
                  ticker)
    for i in dataframe.columns:
        dataframe[i] =  pd.to_numeric(dataframe[i], errors='coerce')
    dataframe = dataframe.loc[:,~dataframe.columns.duplicated()]
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    return dataframe
