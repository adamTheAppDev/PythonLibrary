# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 10:44:11 2017

@author: AmatVictoriaCuramIII
"""

from pandas_datareader import data
import time as t    
import numpy as np
import pandas as pd
from DatabaseGrabber import DatabaseGrabber
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
#    starttime = t.time()    
base = 0
ticker = '^RUT'
q = DatabaseGrabber(ticker)
q2 = pd.DataFrame({'Open':[1407.22],'High':[1407.22],'Low':[1399.26],'Close':[0],'Volume':[0],
'Adj Close':[1403.91]},index = ['2017-06-09 00:00:00']) #interday
q = pd.concat([q,q2])
q['UpMove'] = q['High'] - q['High'].shift(1)
q['DownMove'] = q['Low'] - q['Low'].shift(1)
q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
q['LogRet'] = q['LogRet'].fillna(0)
q['Method1'] = q['High'] - q['Low']
q['Method2'] = abs((q['High'] - q['Adj Close'].shift(1)))
q['Method3'] = abs((q['Low'] - q['Adj Close'].shift(1)))
q['Method1'] = q['Method1'].fillna(0)
q['Method2'] = q['Method2'].fillna(0)
q['Method3'] = q['Method3'].fillna(0)
q['TrueRange'] = q[['Method1','Method2','Method3']].max(axis = 1)
q['PDM'] = (q['High'] - q['High'].shift(1))
q['MDM'] = (q['Low'].shift(1) - q['Low'])
q['PDM'] = q['PDM'][q['PDM'] > 0]
q['MDM'] = q['MDM'][q['MDM'] > 0]
q['PDM'] = q['PDM'].fillna(0)
q['MDM'] = q['MDM'].fillna(0)
#    counter = 0
size = len(Aggregate.iloc[0])
advice = 0
for i in Aggregate:
#        counter = counter + 1  
#        ratio = counter/size
    aa = Aggregate.loc[0,i] #numer of days for moving average window
    a = aa.astype(int)
    b = Aggregate[i].iloc[1]
    c = Aggregate[i].iloc[2] 
    d = Aggregate[i].iloc[3]
    window = a
    q['AverageTrueRange'] = q['TrueRange'].rolling(window = window,
                                    center=False).sum()
    q['AverageTrueRange'] = ((q['AverageTrueRange'].shift(1)*(window-1
                                 ) + q['TrueRange']) / window)
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
    q['Touch'] = np.where(q['DIdivergence'] < c, 1,0) #long signal
    q['Touch'] = np.where(q['DIdivergence'] > d, -1, q['Touch']) #short signal
    q['Sustain'] = 0
    q['Sustain'] = np.where(q['ADX'] >  q['ADXmean'], 0, q['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    q['Sustain'] = np.where(q['ADX'] < q['ADXmean'], (q['Touch']*-1
                          ), q['Sustain']) #never actually true when optimized
    q['Regime'] = q['Touch'] + q['Sustain']
    if len(q) <= 1:
        continue
    toadd = q['Regime'].iloc[-1]
    base = base + toadd
    advice = float(base/size)
    print(advice)
print(advice)
ModADXOptimal = pd.read_pickle('TLTModADXAGGOptimal')
aa = ModADXOptimal.iloc[0]
bb = ModADXOptimal.iloc[1]