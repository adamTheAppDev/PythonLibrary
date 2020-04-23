# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import pandas as pd
#Assign ticker
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='01/01/2006', end='01/01/2050')
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Close location value
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Number of periods in time series
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length-1)
#Index object
index = s.index
#Assign params
a = 20 #number of days for moving average window
b = 43 #numer of days for moving average window
#Prep EMA weights
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
#Calculate ADI
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
#Initialize EMA values
EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values
#Calculate small EMA
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[:], index=s.index)    
#Calculate large EMA
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[:], index=s.index)
#Series to list
s['ADIEMAsmall'] = smallEMAseries
s['ADIEMAlarge'] = largeEMAseries
#Calculate Chaikin indicator
s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
#Horizontal line
s['ZeroLine'] = 0
#Assign params
volumewindow = 21
#Calculate average rolling volume
s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
#Normalize by volume
s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
#Graphical display
s[['ADI','ADIEMAsmall','ADIEMAlarge']].plot(grid=True, figsize = (8,3))
#Trim time series
kk = s[:volumewindow-1]
s = s[volumewindow-1:]
#Directional methodology
s['Touch'] = np.where(s['NormChaikin'] < 0, 1,0) #long signal
s['Touch'] = np.where(s['NormChaikin'] > 0, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                 s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
s['Sustain'] = np.where(s['NormChaikin'] > 0, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['NormChaikin'] < 0, 0, s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] + s['Sustain']
#Apply position to returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Performance metric
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
#s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
#Indicator graphical display
s[['NormChaikin', 'ZeroLine']].plot(grid=True, figsize = (8,3))
#Add data back
s = kk.append(s)
#Performance metric
print(sharpe)
