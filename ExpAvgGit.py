# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This calculation of EMA is non-pythonic/inefficient/process intensive - use np.convolve

#Import modules
from pandas_datareader import data
import numpy as np
import pandas as pd

#Ticker assignment 
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='9/12/2016', end='01/01/2050')
#Variable assignment
a = 12 #number of days for moving average window
b = 26 #numer of days for moving average window
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
#Iterable
Range = range(0, len(s['Adj Close']))
#Calculate log returns, add fillna(0)
s['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))

#Initialize previous period SMA
EMAyesterdayA = s['Adj Close'][0] #these prices are based off the SMA values
EMAyesterdayB = s['Adj Close'][0] #these prices are based off the SMA values
#Initialize list
smallEMA = [EMAyesterdayA]
#For all dates in time series
for i in Range:
    #Temporary variable
    holder = (s['Adj Close'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    #Add to list
    smallEMA.append(holder)
    #Variable ssignment
    EMAyesterdayA = holder
#List to series
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
#Initialize list
largeEMA = [EMAyesterdayB]
#For all dates in time series
for i in Range:
    #Temporary variable
    holder1 = (s['Adj Close'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    #Add to list
    largeEMA.append(holder1)
    #Variable assignment
    EMAyesterdayB = holder1
#List to series
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
#Add series to dataframe
s['SmallEMA'] = smallEMAseries
s['LargeEMA'] = largeEMAseries
#Graph dataframe
s[['SmallEMA', 'LargeEMA', 'Close']].plot(grid=True, figsize=(8, 5))
