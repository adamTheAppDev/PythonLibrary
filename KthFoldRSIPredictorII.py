# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
import pandas as pd
from pandas_datareader import data
import os
#import pandas as pd

#Read in data
Aggregate = pd.read_pickle('RUTAGGSHARPE044')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Zeros
base = 0
#Read in params
size = len(Aggregate.iloc[0])
#Request data
s = data.DataReader('^RUT', 'yahoo', start='01/01/1950', end='01/01/2050') #change to s if after 6pm 
#Add new data before close
#s2 = pd.DataFrame({'Open':[1392.03],'High':[1400.81],'Low':[1390.44],'Close':[0],'Volume':[0],
#'Adj Close':[1398.36]},index = ['2017-05-10 00:00:00']) #interday
#s = pd.concat([s,s2]) #if after 6pm then comment out
#For all params sets
for i in Aggregate:
    #Read in params
    a = Aggregate[i].iloc[0]
    aa = a.astype(int)
    b = Aggregate[i].iloc[1]
    c = Aggregate[i].iloc[2]
    d = Aggregate[i].iloc[3]
    e = Aggregate[i].iloc[4]
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    #Calculate RSI
    close = s['Adj Close']
    window = aa 
    delta = close.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    AvgGain = up.rolling(window).mean()
    AvgLoss = down.abs().rolling(window).mean() 
    RS = AvgGain/AvgLoss
    RSI = 100 - (100/(1.0+RS))
    s['RSI'] = RSI
    s['RSI'] = s['RSI'].fillna(0)
    #Directional methodology
    s['Touch'] = np.where(s['RSI'] < b, 1,0) #long signal
    s['Touch'] = np.where(s['RSI'] > c, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                  s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                s['Sustain']) 
    s['Sustain'] = np.where(s['RSI'] > d, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['RSI'] < e, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    #Get directional assumption
    toadd = s['Regime'][-1]
    #Add to aggregate directional statistic
    base = base + toadd 
    #Total aggregate directional statistic
    advice = base/size
#Print results
print(advice)
