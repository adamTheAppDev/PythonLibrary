# -*- coding: utf-8 -*-
"""

@author: AmatVictoriaCuramIII

"""

#This is an Edge Ratio calculator for single issue
#May be deprecated see ERatioSingleIssueDonchianTrendIII.py
#E-ratio SMA no filter

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import pandas as pd

#Empty data structures
edgelist = []
tempdf = pd.DataFrame()
#Variable assignment
lag = 15
atrwindow = 20
smawindow = 10
edgedays = 20
iterations = range(2,20)
ticker = 'UVXY'

#Request data
s = YahooGrabber(ticker)
#Start timer
#start = t.time()
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Iterable index
s['idx'] = range(0,len(s))
#Simple moving average calculation
s['SMA'] = s['Adj Close'].rolling(window=smawindow, center=False).mean()

#ATR calculation
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
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
#Horizontal line
s['ZeroLine'] = 0
#Directional methodology
s['Regime'] = np.where(s['Adj Close'] > s['SMA'], -1, 0)
#Zeros
s['OriginalTrade'] = 0
#Signal if no signal in prior period/row
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = 1  

#Make list of Original Trade DATES
tradedates = s[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               s['Regime'].shift(1) == 0) & (s['Regime'] == -1)]
#Number of signals
numsignals = len(tradedates)
#Zeros
tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#compute MFE and MAE for z day period
for z in iterations:
    #For all signals in time series
    for i in tradedates.idx:
        #Select data for z days
        tempdf['Adj Close'] = s['Adj Close'].loc[s.index[i:i+z]]
        #MFE/MAE
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        #Empty data structure
        tempdf = pd.DataFrame()  
        #Assign MFE/MAE
        tradedates['MFEpoints'].loc[tradedates.idx == i] = maxup
        tradedates['MAEpoints'].loc[tradedates.idx == i] = mindown
    #Adjust for volatility - ATR
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    #Sum all MFE/MAE
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    #Divide by number of signals to get average
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    #Calculate edge ratio
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    #Apply directional methodology to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Returns on $1
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown statistic
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Performance metrics
    dailyreturn = s['Strategy'].mean()
    dailyvol = s['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    #Graphical display
#    s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    #Display results
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
              
#Variable assignment      
Length = len(s['LogRet'])
Range = range(0,Length)
#Incorrectly calculated statistic
print(MaxDD*100, '% = Max Drawdown')
#Make data structure
edgeratioframe = pd.DataFrame(index = iterations)
#Add data to structure
edgeratioframe['EdgeRatio'] = edgelist
#Line graph of edge ratio
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#End timer
end = t.time()
#Timer stats
print((end - start), ' seconds later.')
#Highest edge ratio
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
