# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an Edge Ratio calculator for single issue
#May be deprecated see ERatioSingleIssueDonchianTrendIII.py
#SMA edge ratio w/ VIX

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd

#Empty data structures
tempdf = pd.DataFrame()
edgelist = []

#Assign variables
ticker1 = 'UVXY'
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
iterations = range(2,120)

#Request data
Asset1 = YahooGrabber(ticker1)
#Start timer
start = t.time()
#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
#Psuedo index iterable
Asset1['idx'] = range(0,len(Asset1))
#Simple moving average calculation
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=smawindow, center=False).mean()

#ATR calculation
Asset1['UpMove'] = Asset1['High'] - Asset1['High'].shift(1)
Asset1['DownMove'] = Asset1['Low'] - Asset1['Low'].shift(1)
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
#Horizontal line
Asset1['ZeroLine'] = 0
#Directional methodology
Asset1['Regime'] = np.where(Asset1['Adj Close'] < Asset1['SMA'], -1, 0)
#Zeros
Asset1['OriginalTrade'] = 0
#1 if no signal in prior period/row
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = 1  

#Make list of Original Trade DATES
tradedates = Asset1[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)]
#Total number of signals
numsignals = len(tradedates)
#Zeros
tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#compute MFE and MAE for z number of days
for z in iterations:
    #For all dates where there is a signal
    for i in tradedates.idx:
        #Select data for period
        tempdf['Adj Close'] = Asset1['Adj Close'].loc[Asset1.index[i:i+z]]
        #MAE/MFE
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        #Empty data structure
        tempdf = pd.DataFrame()
        #Assign MFE/MAE
        tradedates['MFEpoints'].loc[tradedates.idx == i] = mindown
        tradedates['MAEpoints'].loc[tradedates.idx == i] = maxup
    #Adjust for volatilty with ATR    
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    #Add all stats
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    #Divide by number of signals to get average
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    #Calculate z day edge ratio
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    #Apply directional methodology to returns
    Asset1['Strategy'] = (Asset1['Regime']).shift(1)*Asset1['LogRet']
    Asset1['Strategy'] = Asset1['Strategy'].fillna(0)
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown statistic
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    Asset1['drawdown'] =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    
    #Performance metrics
    dailyreturn = Asset1['Strategy'].mean()
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    #Graphical dispaly
#    s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    #Display results
    print('The ', z, ' day edge ratio is', edgeratio)
    #Add data to list
    edgelist.append(edgeratio)

#Variable assignment    
Length = len(Asset1['LogRet'])
#Iterable
Range = range(0,Length)

#Incorrectly calculated
print(MaxDD*100, '% = Max Drawdown')

#Make dataframe structure
edgeratioframe = pd.DataFrame(index = iterations)
#Add data to structure
edgeratioframe['EdgeRatio'] = edgelist
#Edge ratio line graph
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#End timer
end = t.time()
#Timer stats
print((end - start), ' seconds later.')
#Highest edge ratio
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
