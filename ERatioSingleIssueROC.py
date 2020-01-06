# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:13:31 2019

@author: AmatVictoriaCuramIII
"""

#N Period Edge Ratio Computation

#Import-ant
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
 
#Let's go
start = t.time()

#Empty structures
tempdf = pd.DataFrame()
edgelist = []

#Variable assignment

#Issue selection
ticker = 'UVXY'

#Data import
Asset = YahooGrabber(ticker)

#Params
atrwindow = 20
donchianwindow = 20
edgedays = 20
lag = 20

#N Period selection // range(2,3) = day after trade is entered 'on close'
iterations = range(2,21) 

#Trimmer for convenience
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

#ROC calculation
Asset['RateOfChange'] = (Asset['Adj Close'] - Asset['Adj Close'].shift(lag)
                                  ) / Asset['Adj Close'].shift(lag)
                                  
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
Asset['Regime'] =  np.where(Asset['RateOfChange'] >  0.3, -1, np.nan)
#Asset['Regime'] = np.where(Asset['Low'] < Asset['RollingMin'].shift(1), -1, Asset['Regime'])
Asset['Regime'] = Asset['Regime'].ffill(limit = 80)
#Stay flat if ATR has not been established // nan > 0 == false
#Asset['Regime'] = np.where(Asset['AverageTrueRangePercent'] > 0, Asset['Regime'], 0)
#Asset['Regime'] = Asset['Regime'].ffill(limit=80)
Asset['Regime'] = Asset['Regime'].fillna(0)
#Zeros assignment
Asset['OriginalTrade'] = 0
#Establish the original trade at the first directional signal in a regime// short then long
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == -1)] = -1  
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == 1)] = 1 

#Make list of Original TRADE DATES; include relevant data for E ratio calculation
tradedates = Asset[['Regime', 'Index', 'RangeIndex', 'Adj Close', 'AverageTrueRangePoints']].loc[(
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
        tempdf = pd.DataFrame()
        tempdf['Close'] = Asset['Close'].loc[Asset.index[i:i+z]] 
        tempdf['High'] = Asset['High'].loc[Asset.index[i:i+z]] 
        tempdf['Low'] = Asset['Low'].loc[Asset.index[i:i+z]] 
        print(tempdf)
        if tradedates['Regime'].loc[tradedates['RangeIndex'] == i][0] == 1:
            maxup = max(tempdf['High'] - tempdf['Close'][0])
            maxdown = max(tempdf['Close'][0] - tempdf['Low']) 
            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown

        if tradedates['Regime'].loc[tradedates['RangeIndex'] == i][0] == -1:
            maxup = max(tempdf['Close'][0] - tempdf['Low']) 
            maxdown = max(tempdf['High'] - tempdf['Close'][0]) 
            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown
            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
    
        
    tradedates['VolAdjMFE'] = tradedates['MFEpoints']/tradedates['AverageTrueRangePoints']
    tradedates['VolAdjMAE'] = tradedates['MAEpoints']/tradedates['AverageTrueRangePoints']
    
    sumMFE = sum(tradedates['VolAdjMFE'])
    sumMAE = sum(tradedates['VolAdjMAE'])
    
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
    
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
Asset['Strategy'] = Asset['Strategy'].fillna(0)
Asset['Multiplier'] = Asset['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
Asset['drawdown'] =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())

MaxDD = max(drawdown)


dailyreturn = Asset['Strategy'].mean()

dailyvol = Asset['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
#Asset[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
    

              
Length = len(Asset['LogRet'])
Range = range(0,Length)
print(MaxDD*100, '% = Max Drawdown')

edgeratioframe = pd.DataFrame(index = iterations)
edgeratioframe['EdgeRatio'] = edgelist

edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
end = t.time()
print((end - start), ' seconds later.')
print('Max eRatio is', max(edgeratioframe['EdgeRatio']))

##Graphics
##X and Y axis scale figure
#figure, axe = plt.subplots(figsize = (10,5))
##Assign axis labels
#plt.ylabel(ticker + ' Price')
#plt.xlabel('Date') 
##Overlay
##axe.plot(AssetCopy['IndexToNumber'], Asset['RollingMax'], color = 'green', label = 'RollingMax')
##axe.plot(AssetCopy['IndexToNumber'], Asset['RollingMin'], color = 'red', label = 'RollingMin')
##axe.plot(Asset['IndexToNumber'], Asset['SMA'], color = 'black', label = 'SMA')
#
##Signal triangles..
#axe.scatter(Asset.loc[Asset['OriginalTrade'] == 1, 'IndexToNumber'].values, 
#            Asset.loc[Asset['OriginalTrade'] == 1, 'Adj Close'].values, label='skitscat', color='green', s=75, marker="^")
#axe.scatter(Asset.loc[Asset['OriginalTrade'] == -1, 'IndexToNumber'].values, 
#            Asset.loc[Asset['OriginalTrade'] == -1, 'Adj Close'].values, label='skitscat', color='red', s=75, marker="v")
#
##Plot the DF values with the figure, object
#candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
#axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#
##For ATR
#figure2, axe2 = plt.subplots(figsize = (10,2))
#plt.ylabel(ticker + ' ATR Percent')
#plt.xlabel('Date')
#axe2.plot(AssetCopy['IndexToNumber'], Asset ['AverageTrueRangePercent'], color = 'black', label = '4wkATRPercent')
##axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMax'], color = 'green', label = 'ATRRollingMax')
##axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMin'], color = 'red', label = 'ATRRollingMin')
#axe2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))