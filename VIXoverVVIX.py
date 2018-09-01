# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 20:47:34 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
#import random as rand
import pandas as pd
import time as t
empty = []
asone = pd.DataFrame()
start = t.time()
iterations = range(0,1000)
s = data.DataReader('^VIX', 'yahoo', start='1/1/2007', end='01/01/2050') 
s2 = data.DataReader('^VVIX', 'yahoo', start='1/1/2007', end='01/01/2050') 
s3 = data.DataReader('UVXY', 'yahoo', start='1/1/2007', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1))
s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
s['VolOverVolVol'] = (s['Adj Close']/s2['Adj Close'])
s['VolOverVolVol'].plot(grid=True, figsize=(8,5))