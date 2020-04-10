# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a technical analysis tool

#Import modules
from pandas_datareader import data
import numpy as np
import pandas as pd

#Input ticker
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='9/12/2016', end='01/01/2050')
#Assign params
a = 12 #number of days for exp moving average window
b = 26 #numer of days for exp moving average window
c = 9 #number of days for exp moving average window for MACD line
#Calculate weights
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
multiplierC = (2/(c+1))
#Iterable
Range = range(0, len(s['Adj Close']))
#Calculate log returns
s['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
#Initialize EMAs
EMAyesterdayA = s['Adj Close'][0] #these prices are based off the SMA values
EMAyesterdayB = s['Adj Close'][0] #these prices are based off the SMA values
#Value to list
smallEMA = [EMAyesterdayA]
#For number of days to calculate EMA
for i in Range:
    #Calculate temp variable
    holder = (s['Adj Close'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    #Add to list
    smallEMA.append(holder)
    #Set previous EMA value
    EMAyesterdayA = holder
#List to series
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
#Value to list
largeEMA = [EMAyesterdayB]
#For number of days to calculate EMA
for i in Range:
    #Calculate temp variable
    holder1 = (s['Adj Close'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    #Add to list
    largeEMA.append(holder1)
    #Set previous EMA value
    EMAyesterdayB = holder1
#List to series
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
#Series to dataframe
s['SmallEMA'] = smallEMAseries
s['LargeEMA'] = largeEMAseries
#Calculate MACD
s['MACD'] = s['SmallEMA'] - s['LargeEMA']
#First MACD value
MACDEMAyesterday = s['MACD'][0]
#Value to list
MACDEMA = [MACDEMAyesterday]
#For number of days to calculate EMA
for i in Range:
    #Calculate temp variable
    holder2 = (s['MACD'][i]*multiplierC) + (MACDEMAyesterday *
                                            (1-multiplierC))
    #Add to list
    MACDEMA.append(holder2)
    #Set previous EMA value
    MACDEMAyesterday = holder2
#List to Series
MACDEMAseries = pd.Series(MACDEMA[1:], index=s.index)
#Series to dataframe
s['SignalLine'] = MACDEMAseries
#Horizontal line
s['FlatLine'] = 0
#Graphical displays
s[['SmallEMA', 'LargeEMA', 'Close']].plot(grid=True, figsize=(8, 5))
s[['SignalLine','MACD','FlatLine']].plot(grid=True, figsize=(8, 3))
