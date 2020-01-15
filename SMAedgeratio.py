# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:57:24 2018

@author: AmatVictoriaCuramIII
"""

#This is an edge ratio calculator, its dated and probably doesn't work correctly.
#See ERatioSingleIssueDonchianTrendIII.py for latest and greatest

from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd


tempdf = pd.DataFrame()
edgelist = []
ticker = '^VIX'
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
iterations = range(2,200)
s = YahooGrabber(ticker)
start = t.time()
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['idx'] = range(0,len(s))
s['SMA'] = s['Adj Close'].rolling(window=smawindow, center=False).mean()

s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)

#ATR in points not %

s['AverageTrueRangePoints'] = s['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()

s['ZeroLine'] = 0

s['Regime'] = np.where(s['Adj Close'] > s['SMA'], 1, 0)
s['OriginalTrade'] = 0
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1  

#Make list of Original Trade DATES
tradedates = s[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               s['Regime'].shift(1) == 0) & (s['Regime'] == 1)]
numsignals = len(tradedates)

tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#compute MFE and MAE
for z in iterations:
    for i in tradedates.idx:
        tempdf['Adj Close'] = s['Adj Close'].loc[s.index[i:i+z]]
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        tempdf = pd.DataFrame()  
        tradedates['MFEpoints'].loc[tradedates.idx == i] = maxup
        tradedates['MAEpoints'].loc[tradedates.idx == i] = mindown
        
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    
    MaxDD = max(drawdown)
    
    
    dailyreturn = s['Strategy'].mean()
    
    dailyvol = s['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
#    s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
              
Length = len(s['LogRet'])
Range = range(0,Length)
print(MaxDD*100, '% = Max Drawdown')

edgeratioframe = pd.DataFrame(index = iterations)
edgeratioframe['EdgeRatio'] = edgelist

edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
end = t.time()
print((end - start), ' seconds later.')
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
