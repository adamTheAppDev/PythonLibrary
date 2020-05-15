# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a database query tool, expand to make Executive Dashboard

#Import modules
import pandas as pd
import os
from DatabaseGrabber import DatabaseGrabber

#Empty data structures
Table = pd.DataFrame()
List = []
#Get names of all stocks in Universe // Read in universe list
UniverseList = os.listdir('F:\\Users\\Username\\DatabaseLocation') 
#List trimmer
#UniverseList = UniverseList[:10]

#Attach rows to master table - For all tickers in universe
for i in UniverseList:
    #Request data
    Asset1 = DatabaseGrabber(i)
    #Create dictionary
    Information = {"Ticker":i, "4wkRangeOverPrice" : Asset1['Age'][-1]}#, "Low": Asset1['Low'][-1]}
    #Dict to list
    List = [Information]
    #List to dataframe
    Table = Table.append(List)
    #Iteration tracking
    print(i)
#Set index    
Table = Table.set_index('Ticker')
#Sort table
Table = Table.sort_values(by = 'Age')
