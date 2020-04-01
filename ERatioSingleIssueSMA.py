  
# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an Edge Ratio calculator for single issue
#May be deprecated see ERatioSingleIssueDonchianTrendIII.py
#N Period Edge Ratio Computation

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
 
#Start timer
start = t.time()

#Empty data structures
tempdf = pd.DataFrame()
edgelist = []

#Variable assignment
#Issue selection
ticker = 'UVXY'

#Request data
Asset = YahooGrabber(ticker)

#Assign params
atrwindow = 20
smawindow = 50
edgedays = 20

#N Period selection // range(2,3) = day after trade is entered 'on close'
iterations = range(2,25) 

#Trimmer for convenience; If latest data point is original trade date, will throw index error
Asset = Asset[:-1]

#Represent index as column in Asset the DataFrame
Asset['Index'] = Asset.index
#Alternative range based index starting from 1, not 0
Asset['RangeIndex'] = range(1, len(Asset.index) + 1)

#Format for mpl - graphics
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)

#Format Dataframe to feed candlestick_ohlc() - graphics
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()

#Need to subtract one from this value
Asset['LogRet'] = np.log(Asset['Adj Close']/Asset['Adj Close'].shift(1)) 
Asset['LogRet'] = Asset['LogRet'].fillna(0)

#SMA calculation from params
Asset['SMA'] = Asset['Adj Close'].rolling(window=smawindow, center=False).mean()

#ATR set up
Asset['Method1'] = Asset['High'] - Asset['Low']
Asset['Method2'] = abs((Asset['High'] - Asset['Close'].shift(1)))
Asset['Method3'] = abs((Asset['Low'] - Asset['Close'].shift(1)))
Asset['Method1'] = Asset['Method1'].fillna(0)
Asset['Method2'] = Asset['Method2'].fillna(0)
Asset['Method3'] = Asset['Method3'].fillna(0)
Asset['TrueRange'] = Asset[['Method1','Method2','Method3']].max(axis = 1)

#ATR in points from params
Asset['AverageTrueRangePoints'] = Asset['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()
#ATR in percent
Asset['AverageTrueRangePercent'] = Asset['AverageTrueRangePoints'] / Asset['Close']

#Directional methodology
Asset['Regime'] = np.where(Asset['Adj Close'] < Asset['SMA'], -1, 0)

#Stay flat if ATR has not been established // nan > 0 == false
Asset['Regime'] = np.where(Asset['AverageTrueRangePercent'] > 0, Asset['Regime'], 0)

#Zeros assignment
Asset['OriginalTrade'] = 0
#Establish the original trade at the first directional signal in a regim// short then long
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == -1)] = -1  
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == 1)] = 1 

#Make list of Original TRADE DATES; include relevant data for E ratio calculation
tradedates = Asset[['OriginalTrade', 'Index', 'RangeIndex', 'Adj Close', 'AverageTrueRangePoints']].loc[(
                               Asset['OriginalTrade'] != 0)]
#Sample size
numsignals = len(tradedates)

#Zeros assign
tradedates['MFEpoints'] = 0
tradedates['MAEpoints'] = 0

#compute MFE and MAE
#For the amount of days specified in params
for z in iterations:
    #For all dates in tradedates    
    for i in tradedates.RangeIndex:
        #Empty data structure
        tempdf = pd.DataFrame()
        #Fill with price data
        tempdf['Close'] = Asset['Close'].loc[Asset.index[i:i+z]] 
        tempdf['High'] = Asset['High'].loc[Asset.index[i:i+z]] 
        tempdf['Low'] = Asset['Low'].loc[Asset.index[i:i+z]] 
        #Print display
        print(tempdf)
        #For long trades
        if tradedates['OriginalTrade'].loc[tradedates['RangeIndex'] == i][0] == 1:
            #MFE assignment
            maxup = max(tempdf['High'] - tempdf['Close'][0])
            #MAE assignment 
            maxdown = max(tempdf['Close'][0] - tempdf['Low']) 
            #Assign to dataframe
            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown
        #For short trades
        if tradedates['OriginalTrade'].loc[tradedates['RangeIndex'] == i][0] == -1:
            #MFE assignment
            maxup = max(tempdf['Close'][0] - tempdf['Low']) 
            #MAE assignment
            maxdown = max(tempdf['High'] - tempdf['Close'][0]) 
            #Assign to dataframe
            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown
            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
    
    #Adjust for volatility -- ATR normalization    
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    #Add together
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    #Average by dividing by number of signals
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    #Calculate edge ratio
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    
    #Apply directional methodology to returns
    Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
    Asset['Strategy'] = Asset['Strategy'].fillna(0)
    #Returns on $1
    Asset['Multiplier'] = Asset['Strategy'].cumsum().apply(np.exp)
    
    #Incorrectly calculated drawdown stat - fix
    drawdown =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
    Asset['drawdown'] =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
    MaxDD = max(drawdown)
    
    #Performance metrics
    dailyreturn = Asset['Strategy'].mean()
    dailyvol = Asset['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    
    #Print results
    print('The ', z, ' day edge ratio is', edgeratio)
    #Add metric to list
    edgelist.append(edgeratio)
              
#Variable assignment
Length = len(Asset['LogRet'])
Range = range(0,Length)
#Incorrectly calculated
print(MaxDD*100, '% = Max Drawdown')
#Assign data structure
edgeratioframe = pd.DataFrame(index = iterations)
#Add data to structure
edgeratioframe['EdgeRatio'] = edgelist
#Graphical display
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#End timer
end = t.time()
#Timer stats
print((end - start), ' seconds later.')
#Print highest e-ratio
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))
