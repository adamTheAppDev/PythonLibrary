# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:20:21 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import pandas as pd
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='07/01/2016', end='12/01/2016') 
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
Length = len(s['LogRet'])
Range = range(0,Length)
ADI = []
store = 0
index = s.index
for i in Range:
        store = store + (s['Volume'][i] * s['CLV'][i])
        ADI.append(store)
ADISeries = pd.Series(ADI, index=index)
ADISeries.plot(grid=True, figsize = (8,3))
