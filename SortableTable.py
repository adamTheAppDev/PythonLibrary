# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 23:01:51 2018

@author: AmatVictoriaCuramIII
"""

#Executive Dashboard ;]
#Import 
import pandas as pd
import os
from DatabaseGrabber import DatabaseGrabber
#Let's make a sortable table
Table = pd.DataFrame()
List = []
#Get names of all stocks in Universe
UniverseList = os.listdir('F:\\Users\\AmatVictoriaCuram\\Database') 
#List trim
#UniverseList = UniverseList[:10]

#We attach rows to master table
for i in UniverseList:
    Asset1 = DatabaseGrabber(i)
    Information = {"Ticker":i, "4wkRangeOverPrice" : Asset1['Age'][-1]}#, "Low": Asset1['Low'][-1]}
    List = [Information]
    Table = Table.append(List)
    print(i)
    
Table = Table.set_index('Ticker')
Table = Table.sort_values(by = 'Age')