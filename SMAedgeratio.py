# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an edge ratio calculator, its dated and probably doesn't work correctly.
#See ERatioSingleIssueDonchianTrendIII.py for latest and greatest

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd

#Empty data structure
tempdf = pd.DataFrame()
edgelist = []
#Assign ticker
ticker = '^VIX'
#Variable assignment
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
#Iterable
iterations = range(2,200)
#Request data
s = YahooGrabber(ticker)
#Start timer
start = t.time()
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Index copy
s['idx'] = range(0,len(s))
#Calculate simple moving average
s['SMA'] = s['Adj Close'].rolling(window=smawindow, center=False).mean()
#Difference of current high to previous high
s['UpMove'] = s['High'] - s['High'].shift(1)
#Difference of current low to previous low
s['DownMove'] = s['Low'] - s['Low'].shift(1)
#Calculate ATR
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
s['Regime'] = np.where(s['Adj Close'] > s['SMA'], 1, 0)
#Zeros
s['OriginalTrade'] = 0
#Initial signal in stream of sustained signals
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1  

#Make list of Original Trade dates
tradedates = s[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               s['Regime'].shift(1) == 0) & (s['Regime'] == 1)]
#Number of initial signals
numsignals = len(tradedates)
#Zeros
tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#Compute MFE and MAE - remember this is a long only regime
#For desired number of periods to compute e-ratio for 
for z in iterations:
    #For every trade date
    for i in tradedates.idx:
        #Get close prices from signal to z periods 
        tempdf['Adj Close'] = s['Adj Close'].loc[s.index[i:i+z]]
        #Maximum upwards price movement
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        #Maximum downwards price movement
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        #Clear dataframe
        tempdf = pd.DataFrame()  
        #Log MAE and MFE in points
        tradedates['MFEpoints'].loc[tradedates.idx == i] = maxup
        tradedates['MAEpoints'].loc[tradedates.idx == i] = mindown
    #Adjust for volatility based on ATR    
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    #Add total volatility adjusted MFE and MAE
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    #Divide by number of signals to get average MFE and MAE
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    #Compute edge ratio
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Returns on $1
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown stat
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Performance metrics
    dailyreturn = s['Strategy'].mean()
    dailyvol = s['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    #Display results 
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
#Number of periods in time series              
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length)
#Display results
print(MaxDD*100, '% = Max Drawdown')
#Create dataframe for e-ratio stats
edgeratioframe = pd.DataFrame(index = iterations)
#List to series
edgeratioframe['EdgeRatio'] = edgelist
#Line graph of edge ratio
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#End timer
end = t.time()
#Timer stats
print((end - start), ' seconds later.')
#Display results
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
