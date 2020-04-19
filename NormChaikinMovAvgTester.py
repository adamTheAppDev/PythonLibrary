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
s = data.DataReader(ticker, 'yahoo', start='07/01/2013', end='12/01/2016') 
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Calculate Close Location Value 
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Number of periods in time series
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length)
#Empty data strucutres
ADI = []
store = 0
#Assign index variable
index = s.index
#Assign EMA params
a = 6 #number of days for moving average window
b = 14 #numer of days for moving average window
#Prep weights
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
#For all periods in time series
for i in Range:
        #Temp variable
        store = store + (s['Volume'][i] * s['CLV'][i])
        #Save to list
        ADI.append(store)
#List to series
ADISeries = pd.Series(ADI, index=index)
#Series to dataframe
s['ADI'] = ADISeries
#Intialize EMA  
EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values
#Calculate small EMA
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
#Calculate large EMA
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
#Series to dataframe
s['ADIEMAsmall'] = smallEMAseries
s['ADIEMAlarge'] = largeEMAseries
#Chaikin indicator
s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
#Horizontal line
s['ZeroLine'] = 0
#Assign param
volumewindow = 36
#Calculate average rolling volume
s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
#Normalize by volume
s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
#SMA 
s['NormChaikinMovAvg'] = s['NormChaikin'].rolling(window=53,center=False).mean()
#SMA spread
s['MovAvgDivergence'] = s['NormChaikin'] - s['NormChaikinMovAvg']
#s[['ADI','ADIEMAsmall','ADIEMAlarge']].plot(grid=True, figsize = (8,3))
#Time series trim
s = s[volumewindow-1:]
#Indicator graphical display
s[['NormChaikin','ZeroLine','NormChaikinMovAvg']].plot(grid=True, figsize = (8,3))
#Directional methodology
s['Touch'] = np.where(s['MovAvgDivergence'] < 1.747773, 1,0) #long signal
s['Touch'] = np.where(s['MovAvgDivergence'] > .169902, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                   s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
s['Sustain'] = np.where(s['MovAvgDivergence'] > -.110568, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['MovAvgDivergence'] < -1.882921, 0, s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] + s['Sustain']
#Apply position to log returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Performance metric
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
#Graphical display
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                figsize=(8,5))
#Display results
print(sharpe)
