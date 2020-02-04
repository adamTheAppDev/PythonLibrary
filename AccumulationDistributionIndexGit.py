# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a techincal indicator.

#Import modules
import numpy as np
from YahooGrabber import YahooGrabber
import pandas as pd

#Input ticker
ticker = '^GSPC'

#Data request - Use YahooGrabber
s = data.DataReader(ticker, 'yahoo', start='07/01/2016', end='12/01/2016') 

#Log return calculation
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Current money flow value
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Make iterator
Length = len(s['LogRet'])
Range = range(0,Length)

#Empty list
ADI = []
store = 0

#index variable
index = s.index

#Calculate ADI
for i in Range:
        store = store + (s['Volume'][i] * s['CLV'][i])
        ADI.append(store)
#Create indicator graphical display
ADISeries = pd.Series(ADI, index=index)
ADISeries.plot(grid=True, figsize = (8,3))
