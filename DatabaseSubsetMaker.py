# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:51:40 2017

@author: AmatVictoriaCuramIII
"""

#This program is not concise, but it is a faster way 
#Essentially a database query tool that returns specific columns from all tickers in database

#column grabber and concatenation
from DatabaseGrabber import DatabaseGrabber
import pandas as pd
import time as t
import webbrowser as web
from pandas import read_csv
from datetime import date
import datetime
import os
import numpy as np
counter = 0
df2 = pd.DataFrame()
df = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\goodsymbols.csv', sep = ',')
#whole range
ranger = range(0,len(df['Symbol']))
#multiple range subsets
ranger1 = ranger[:1000]
ranger2 = ranger[1000:2000]
ranger3 = ranger[2000:3000] 
ranger4 = ranger[3000:4000] 
ranger5 = ranger[4000:5000] 
ranger6 = ranger[5000:len(df['Symbol'])] 
def segment(df2, ranger,counter):
    for i in ranger:
        try:
            x = str(df['Symbol'][i])
            temp = DatabaseGrabber(x)
            temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
            temp[x+'LogRet'] = temp['LogRet'] 
            temp[x+'LogRet'] = temp[x+'LogRet'].fillna(0)            
            df2 = pd.concat([df2,temp[x+'LogRet']],axis = 1)
            print(counter)
            counter += 1
        except OSError:
            counter += 1
            continue
        except FileNotFoundError:
            counter += 1
            continue
    return df2
slice1 = segment(df2, ranger1, counter)
slice1 = slice1.fillna(0)
slice2 = segment(df2, ranger2, counter)
slice3 = segment(df2, ranger3, counter)
slice4 = segment(df2, ranger4, counter)
slice5 = segment(df2, ranger5, counter)
slice6 = segment(df2, ranger6, counter)
bigmama = pd.concat([slice1,slice2,slice3,slice4,slice5,slice6],axis=1)
bigmama = bigmama.fillna(0)

if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\UniverseLogRet'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\UniverseLogRet')
    
pd.to_pickle(bigmama, 'F:\\Users\\AmatVictoriaCuram\\Database\\UniverseLogRet\\UniverseLogRet')
