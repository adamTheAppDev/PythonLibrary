# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is part of a kth fold optimization tool

#Import modules
from pandas_datareader import data
import time as t    
import numpy as np
import pandas as pd
from DatabaseGrabber import DatabaseGrabber
#Read in data
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
#Start timer
#    starttime = t.time()    
#Variable assignment
base = 0
ticker = '^RUT'
#Request data
q = DatabaseGrabber(ticker)
#Insert additional row
q2 = pd.DataFrame({'Open':[1407.22],'High':[1407.22],'Low':[1399.26],'Close':[0],'Volume':[0],
'Adj Close':[1403.91]},index = ['2017-06-09 00:00:00']) #interday
#Row concatenation
q = pd.concat([q,q2])

#Calculate log returns
q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
q['LogRet'] = q['LogRet'].fillna(0)
#Calculate ATR
q['UpMove'] = q['High'] - q['High'].shift(1)
q['DownMove'] = q['Low'] - q['Low'].shift(1)
q['Method1'] = q['High'] - q['Low']
q['Method2'] = abs((q['High'] - q['Adj Close'].shift(1)))
q['Method3'] = abs((q['Low'] - q['Adj Close'].shift(1)))
q['Method1'] = q['Method1'].fillna(0)
q['Method2'] = q['Method2'].fillna(0)
q['Method3'] = q['Method3'].fillna(0)
q['TrueRange'] = q[['Method1','Method2','Method3']].max(axis = 1)

#Calculate ADX
q['PDM'] = (q['High'] - q['High'].shift(1))
q['MDM'] = (q['Low'].shift(1) - q['Low'])
q['PDM'] = q['PDM'][q['PDM'] > 0]
q['MDM'] = q['MDM'][q['MDM'] > 0]
q['PDM'] = q['PDM'].fillna(0)
q['MDM'] = q['MDM'].fillna(0)
#    counter = 0
#Assign param 
size = len(Aggregate.iloc[0])
#Zeros
advice = 0
#For every param set
for i in Aggregate:
    #Iteration tracking
#    counter = counter + 1  
#    ratio = counter/size
    #Assign params
    aa = Aggregate.loc[0,i] #numer of days for moving average window
    a = aa.astype(int)
    b = Aggregate[i].iloc[1]
    c = Aggregate[i].iloc[2] 
    d = Aggregate[i].iloc[3]
    window = a
    #ATR calculation
    q['AverageTrueRange'] = q['TrueRange'].rolling(window = window,
                                    center=False).sum()
    q['AverageTrueRange'] = ((q['AverageTrueRange'].shift(1)*(window-1
                                 ) + q['TrueRange']) / window)
    #ADX calculation
    q['SmoothPDM'] = q['PDM'].rolling(window = window,
                                    center=False).sum()
    q['SmoothPDM'] = ((q['SmoothPDM'].shift(1)*(window-1
                                 ) + q['PDM']) / window)
    q['SmoothMDM'] = q['MDM'].rolling(window = window,
                                    center=False).sum()
    q['SmoothMDM'] = ((q['SmoothMDM'].shift(1)*(window-1
                                 ) + q['MDM']) / window)
    q['PDI'] = (100*(q['SmoothPDM']/q['AverageTrueRange']))
    q['MDI'] = (100*(q['SmoothMDM']/q['AverageTrueRange']))
    q['DIdiff'] = abs(q['PDI'] - q['MDI'])
    q['DIdivergence'] = q['PDI'] - q['MDI']
    q['DIsum'] = q['PDI'] + q['MDI']
    q['DX'] = (100 * (q['DIdiff']/q['DIsum']))
    q['DX'] = q['DX'].fillna(0)
    q['ADX'] = q['DX'].rolling(window = window, center = False).mean()
    q['ADXmean'] = q['ADX'].mean() * b
    #Directional methodology
    q['Touch'] = np.where(q['DIdivergence'] < c, 1,0) #long signal
    q['Touch'] = np.where(q['DIdivergence'] > d, -1, q['Touch']) #short signal
    q['Sustain'] = 0
    q['Sustain'] = np.where(q['ADX'] >  q['ADXmean'], 0, q['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    q['Sustain'] = np.where(q['ADX'] < q['ADXmean'], (q['Touch']*-1
                          ), q['Sustain']) #never actually true when optimized
    q['Regime'] = q['Touch'] + q['Sustain']
    #Contraint
    if len(q) <= 1:
        continue
    #Iteratively add to directional assumption stat     
    toadd = q['Regime'].iloc[-1]
    base = base + toadd
    advice = float(base/size)
    print(advice)
#Display results
print(advice)
