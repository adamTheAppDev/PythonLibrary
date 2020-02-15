# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool, EMA calculation is inefficient, use convolve.

#Import modules
import numpy as np
from pandas_datareader import data
import pandas as pd
from YahooGrabber import YahooGrabber

#Variable assignment
ticker = '^GSPC'

#Request data
s = YahooGrabber(ticker)

#Log return calculation
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Volume scaler calculation
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))

#Iterable based on length --> redundant..
Length = len(s['LogRet'])
Range = range(0,Length)

#Empty variables
ADI = []
store = 0

#Alternative index
index = s.index

#EMA parameters
a = 3 #number of days for moving average window
b = 10 #numer of days for moving average window
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))

#ADI calculation
for i in Range:
        store = store + (s['Volume'][i] * s['CLV'][i])
        ADI.append(store)

#Add ADI to DataFrame
ADISeries = pd.Series(ADI, index=index)
s['ADI'] = ADISeries

#EMA starting points
EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values

#EMA calculation -- use convolve to speed up
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    

#EMA calculation -- use convolve to speed up
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)

#Add EMA data to DataFrame
s['ADIEMAsmall'] = smallEMAseries
s['ADIEMAlarge'] = largeEMAseries

#Chaikin indicator calcuation
s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']

#Horizontal baseline
s['ZeroLine'] = 0

#Avg volume param
volumewindow = 10
s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()

#Normaliz for volume
s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
#s[['ADI','ADIEMAsmall','ADIEMAlarge']].plot(grid=True, figsize = (8,3))

#Trim data for indicator graph
s = s[volumewindow-1:]

#Display 
s[['NormChaikin','ZeroLine']].plot(grid=True, figsize = (8,3))
