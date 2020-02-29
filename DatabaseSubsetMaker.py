# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This program is not concise, but it is a faster way due to batch processing
#Essentially a database query tool that returns specific columns from all tickers in database
#Column grabber and concatenation tool

#Import modules
from DatabaseGrabber import DatabaseGrabber
import pandas as pd
import time as t
import webbrowser as web
from pandas import read_csv
from datetime import date
import datetime
import os
import numpy as np

#Variable assignment
counter = 0
df2 = pd.DataFrame()

#Read in symbols from universe
df = read_csv('F:\\Users\\Username\\DirectoryLocation\\goodsymbols.csv', sep = ',')

#Iterable for symbols
ranger = range(0,len(df['Symbol']))
#Multiple range (batch) subsets for improved processing -- theres a better way to do this with np.arraysplit 
ranger1 = ranger[:1000]
ranger2 = ranger[1000:2000]
ranger3 = ranger[2000:3000] 
ranger4 = ranger[3000:4000] 
ranger5 = ranger[4000:5000] 
ranger6 = ranger[5000:len(df['Symbol'])] 

#Define function
def segment(df2, ranger,counter):
    #For tickers in batch
    for i in ranger:
        try:
            #Ticker as sting
            x = str(df['Symbol'][i])
            #Request data
            temp = DatabaseGrabber(x)
            #Log return calculations
            temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
            #Column name assignment
            temp[x+'LogRet'] = temp['LogRet'] 
            temp[x+'LogRet'] = temp[x+'LogRet'].fillna(0)            
            #Add column to DataFrame
            df2 = pd.concat([df2,temp[x+'LogRet']],axis = 1)
            #Iteration tracking
            print(counter)
            counter += 1
            
        except OSError:
            counter += 1
            continue
            
        except FileNotFoundError:
            counter += 1
            continue
    #Output dataframe with all log returns by ticker        
    return df2
#Run function over batches
slice1 = segment(df2, ranger1, counter)
slice1 = slice1.fillna(0)
slice2 = segment(df2, ranger2, counter)
slice3 = segment(df2, ranger3, counter)
slice4 = segment(df2, ranger4, counter)
slice5 = segment(df2, ranger5, counter)
slice6 = segment(df2, ranger6, counter)

#Aggregating all data from batches
aggregate = pd.concat([slice1,slice2,slice3,slice4,slice5,slice6],axis=1)
aggregate = aggregate.fillna(0)

#Make storage directory
if not os.path.exists('F:\\Users\\Username\\DirectoryLocation\\UniverseLogRet'):
    os.makedirs('F:\\Users\\Username\\DirectoryLocation\\UniverseLogRet')
    
#Save data to local storage    
pd.to_pickle(aggregate, 'F:\\Users\\Username\\DirectoryLocation\\UniverseLogRet\\UniverseLogRet')
