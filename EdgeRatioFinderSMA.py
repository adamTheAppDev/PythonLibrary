# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:57:24 2018

@author: AmatVictoriaCuramIII
"""

#This is an Edge Ratio calculator for single issue
#May be deprecated see ERatioSingleIssueDonchianTrendIII.py
#SMA edge ratio w/ VIX

from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd


tempdf = pd.DataFrame()
edgelist = []
ticker1 = 'UVXY'
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
iterations = range(2,120)
Asset1 = YahooGrabber(ticker1)
start = t.time()
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['idx'] = range(0,len(Asset1))
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=smawindow, center=False).mean()

Asset1['UpMove'] = Asset1['High'] - Asset1['High'].shift(1)
Asset1['DownMove'] = Asset1['Low'] - Asset1['Low'].shift(1)
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)

#ATR in points not %

Asset1['AverageTrueRangePoints'] = Asset1['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()

Asset1['ZeroLine'] = 0

Asset1['Regime'] = np.where(Asset1['Adj Close'] < Asset1['SMA'], -1, 0)
Asset1['OriginalTrade'] = 0
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = 1  

#Make list of Original Trade DATES
tradedates = Asset1[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)]
numsignals = len(tradedates)

tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#compute MFE and MAE
for z in iterations:
    for i in tradedates.idx:
        tempdf['Adj Close'] = Asset1['Adj Close'].loc[Asset1.index[i:i+z]]
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        tempdf = pd.DataFrame()  
        tradedates['MFEpoints'].loc[tradedates.idx == i] = mindown
        tradedates['MAEpoints'].loc[tradedates.idx == i] = maxup
        
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    
    Asset1['Strategy'] = (Asset1['Regime']).shift(1)*Asset1['LogRet']
    Asset1['Strategy'] = Asset1['Strategy'].fillna(0)
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    Asset1['drawdown'] =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    
    MaxDD = max(drawdown)
    
    
    dailyreturn = Asset1['Strategy'].mean()
    
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
#    s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
              
Length = len(Asset1['LogRet'])
Range = range(0,Length)
print(MaxDD*100, '% = Max Drawdown')

edgeratioframe = pd.DataFrame(index = iterations)
edgeratioframe['EdgeRatio'] = edgelist

edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
end = t.time()
print((end - start), ' seconds later.')
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
