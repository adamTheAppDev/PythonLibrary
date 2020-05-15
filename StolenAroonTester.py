# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester 
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from pandas_datareader import data
import pandas as pd
import numpy as np

#Assign ticker
ticker = '^GSPC'

#Request data
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Iterable
s['Ranger'] = range(len(s))
#Create dataframe
k = pd.DataFrame(index = s['Ranger'])
#Empty list
AroonUp = []
AroonDown = []
AroonDate = []
#Variable assignment
#Time factor
tf = 7
AdjClose = s['Adj Close'].tolist()
AdjCloseSeries = pd.Series(AdjClose)
k['Adj Close'] = AdjCloseSeries
Date = s['Ranger'].tolist()
counter = tf
#Calculate Aroon indicator
while counter < len(s):
    Aroon_Up = ((k['Adj Close'][counter-tf:counter].tolist().index(max
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
    Aroon_Down = ((k['Adj Close'][counter-tf:counter].tolist().index(min
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
    AroonUp.append(Aroon_Up)
    AroonDown.append(Aroon_Down)
    AroonDate.append(Date[counter])
    counter = counter + 1
s = s[tf:]
#List to series
AroonUpSeries = pd.Series(AroonUp, index=s.index)
AroonDownSeries = pd.Series(AroonDown, index=s.index)
#Series to dataframe
s['AroonUp'] = AroonUpSeries
s['AroonDown'] = AroonDownSeries
#Difference between up and down
s['Divergence'] = s['AroonUp'] - s['AroonDown']
s['Touch'] = np.where(s['Divergence'] < 86.065983, 1, 0) #long signal
s['Touch'] = np.where(s['Divergence'] > 92.797133, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                            s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1, 
                        s['Sustain'])
s['Sustain'] = np.where(s['Divergence'] > -22.227923, 0, s['Sustain']) 
s['Sustain'] = np.where(s['Divergence'] < 41.853571, 0, s['Sustain']) 
#Directional methodology
s['Regime'] = s['Touch'] + s['Sustain']
#Apply position to returns 
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Performance metric
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
#Graphical dispalys
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))
