# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis + summary statistic tool

#Import modules
import numpy as np
from pandas_datareader import data
#import random as rand
import pandas as pd
import time as t

#Empty data structures
empty = []
asone = pd.DataFrame()
#Start timer
start = t.time()
#Iterable
iterations = range(0,1000)
#Request data
s = data.DataReader('^VIX', 'yahoo', start='1/1/2007', end='01/01/2050') 
s2 = data.DataReader('^VVIX', 'yahoo', start='1/1/2007', end='01/01/2050') 
s3 = data.DataReader('UVXY', 'yahoo', start='1/1/2007', end='01/01/2050')
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1))
s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
#Price relative
s['VolOverVolVol'] = (s['Adj Close']/s2['Adj Close'])
#Graphical display
s['VolOverVolVol'].plot(grid=True, figsize=(8,5))
