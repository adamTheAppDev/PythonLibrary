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

#Empty data structures
tempdf = pd.DataFrame()
edgelist = []

#Assign ticker
ticker1 = 'UVXY'

#Variable assignment
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
#Iterable
iterations = range(2,120)

#Request data
Asset1 = YahooGrabber(ticker1)

#Start timer
start = t.time()

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Alternative index
Asset1['idx'] = range(0,len(Asset1))
#Calculate simple moving average
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=smawindow, center=False).mean()
#Calculate ATR
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
#Find intial signal in stream of -1s
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = 1  

#Make list of Original Trade dates
tradedates = Asset1[['OriginalTrade', 'idx', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)]
#Number of signals in time series
numsignals = len(tradedates)

#Zeros
tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#Compute MFE and MAE - for number of periods to calculate e-ratio
for z in iterations:
    #For number of signals
    for i in tradedates.idx:
        #Get time series from signal period to signal + z period
        tempdf['Adj Close'] = Asset1['Adj Close'].loc[Asset1.index[i:i+z]]
        #Maximum upward movement in time series
        maxup = max(tempdf['Adj Close'][0] - tempdf['Adj Close'])
        #Maximum downward movement in time series
        mindown = abs(min(tempdf['Adj Close'][0] - tempdf['Adj Close']))
        #Clear dataframe
        tempdf = pd.DataFrame()  
        #Assign MFE / MAE
        tradedates['MFEpoints'].loc[tradedates.idx == i] = mindown
        tradedates['MAEpoints'].loc[tradedates.idx == i] = maxup
    #Normalize MAE and MFE by ATR        
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    #Add all normalized vol adjusted MFE and MAE
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    #Divide by number of signals
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    #Calculate edge ratio
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    #Apply position to log returns 
    Asset1['Strategy'] = (Asset1['Regime']).shift(1)*Asset1['LogRet']
    Asset1['Strategy'] = Asset1['Strategy'].fillna(0)
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    Asset1['drawdown'] =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Performance metrics
    dailyreturn = Asset1['Strategy'].mean()
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    #Display results
    print('The ', z, ' day edge ratio is', edgeratio)
    #Add e-ratio to list
    edgelist.append(edgeratio)
              
#Number of periods in time series          
Length = len(Asset1['LogRet'])
#Iterable
Range = range(0,Length)
#Incorrectly calculated max drawdown
print(MaxDD*100, '% = Max Drawdown')

#Create dataframe
edgeratioframe = pd.DataFrame(index = iterations)
#Populate dataframe with list 
edgeratioframe['EdgeRatio'] = edgelist
#Graphical display
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#Endt timer
end = t.time()
#Timer stats
print((end - start), ' seconds later.')
#Display top e-ratio
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
