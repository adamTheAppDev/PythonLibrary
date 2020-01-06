# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:13:31 2019

@author: AmatVictoriaCuramIII
"""

#N Period Edge Ratio Computation

#Imports 
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
 
#Empty structures
tempdf = pd.DataFrame()
edgelist = []
MFEpoints = None
MFElist = []
MAEpoints = None
MAElist = []
nDay = None

#Variable assignment
#Tickers for testing
tickerlist = ['NUGT', 'JNUG']
ticker = 'NUGT'

#For ATR + MFE/MFA calculation
atrwindow = 20

#For signal generation
donchianwindow = 10

#How many days to calculate e-ratio for
LengthOfTest = range(2, 25) #(2,3) = 2 day Eratio // assuming fill at "Entry Price"

#Initiate testing for loop
#for ticker in tickerlist:

#Get data
Asset = YahooGrabber(ticker)

#In sample Trimmer
Asset = Asset[-1000:]

#Make column that represents X axis 
Asset['Index'] = Asset.index

#Format for mpl
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)

#Format Dataframe to feed candlestick_ohlc()
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()

#Timer begin
start = t.time()

#log returns
Asset['LogRet'] = np.log(Asset['Adj Close']/Asset['Adj Close'].shift(1)) 
Asset['LogRet'] = Asset['LogRet'].fillna(0)

#Donchian Channel calculation from params
Asset['RollingMax'] = Asset['High'].rolling(window=donchianwindow, center=False).max()
Asset['RollingMin'] = Asset['Low'].rolling(window=donchianwindow, center=False).min()

#Index copies
Asset['Index'] = Asset.index
Asset['RangeIndex'] = range(1, len(Asset.index) + 1)

#ATR calculation
Asset['Method1'] = Asset['High'] - Asset['Low']
Asset['Method2'] = abs((Asset['High'] - Asset['Close'].shift(1)))
Asset['Method3'] = abs((Asset['Low'] - Asset['Close'].shift(1)))
Asset['Method1'] = Asset['Method1'].fillna(0)
Asset['Method2'] = Asset['Method2'].fillna(0)
Asset['Method3'] = Asset['Method3'].fillna(0)
Asset['TrueRange'] = Asset[['Method1','Method2','Method3']].max(axis = 1)

#ATR in points not %
Asset['AverageTrueRangePoints'] = Asset['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()
#ATR in percent
Asset['AverageTrueRangePercent'] = Asset['AverageTrueRangePoints'] / Asset['Close']

#Signal generation; long if new high and no new high on previous period, short 
#if new low and no new low on previous period; if Donchian window or ATR is not calculated stay out of market
Asset['Regime'] = np.where(Asset['High'] > Asset['RollingMax'].shift(1), 1, 0)
Asset['Regime'] = np.where(Asset['Low'] < Asset['RollingMin'].shift(1), -1, Asset['Regime'])

#Stay flat if ATR has not been established // nan > 0 == false
Asset['Regime'] = np.where(Asset['AverageTrueRangePercent'] > 0, Asset['Regime'], 0)

#Find trade date when regime changes
Asset['OriginalTrade'] = 0
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == -1)] = -1  
Asset['OriginalTrade'].loc[(Asset['Regime'].shift(1) != Asset['Regime']) & (Asset['Regime'] == 1)] = 1 

#Organize entry price & check for gap
Asset['EntryPrice'] = np.nan
#For all original trade days
for a in Asset['OriginalTrade'][Asset['OriginalTrade'] != 0].index:
    #If a long trade
    if Asset['OriginalTrade'][a] == 1:
        #Record previous high as entry
        Asset['EntryPrice'].loc[a] = Asset['RollingMax'].shift(1).loc[a]
        #Check for open higher than entry gap and reassign
        if Asset['Open'][a] > Asset['EntryPrice'][a]:
            Asset['EntryPrice'].loc[a] = Asset['Open'][a]
    #If a short trade
    if Asset['OriginalTrade'][a] == -1:
        #Record previous high as entry
        Asset['EntryPrice'].loc[a] = Asset['RollingMin'].shift(1).loc[a]
        #Check for open lower than entry gap and reassign
        if Asset['Open'][a] < Asset['EntryPrice'][a]:
            Asset['EntryPrice'].loc[a] = Asset['Open'][a]
            
Asset['EntryPrice'] = Asset['EntryPrice'].ffill()   
            
#Make list of Original Trade DATES
tradedates = Asset[['OriginalTrade', 'Index', 'RangeIndex', 'Adj Close', 'AverageTrueRangePoints', 'EntryPrice']].loc[(
                               Asset['OriginalTrade'] != 0)]
#Number of signals generated
numsignals = len(tradedates)

#For number of e-ratio days to compute
for z in LengthOfTest:
    print('Calculating ' + str(z) + ' Day e-ratio')
    #For each value of RangeIndex on Tradedate
    for i in tradedates.RangeIndex:
        print('Calculating ' + str(z) + ' Day e-ratio for trade on ' + str(Asset['Index'].loc[Asset['RangeIndex'] == i][0]))
        #Assign computation space
        tempdf = pd.DataFrame()
        #Assign entry price
        entryprice = Asset['EntryPrice'].loc[Asset['RangeIndex'] == i][0]
        #Take H, L, C, sample data for number of days under study post trade        
        tempdf['Close'] = Asset['Close'].loc[Asset.index[i:i+z]] 
        tempdf['High'] = Asset['High'].loc[Asset.index[i:i+z]] 
        tempdf['Low'] = Asset['Low'].loc[Asset.index[i:i+z]] 

        #For long trades 
        if tradedates['OriginalTrade'].loc[tradedates['RangeIndex'] == i][0] == 1:  
            if len(tempdf) < z-1 :
                MFElist.append(np.nan)
                MAElist.append(np.nan)
                print('Not enough data for this calculation')                
                continue
            print('Long entry at ', entryprice) 
            #Check status 
#            print(tempdf)
            #MFE
            maxup = max(tempdf['High'] - entryprice)
            #MAE            
            maxdown = max(entryprice - tempdf['Low']) 
            print('MFE in points = ', maxup)
            print('MAE in points = ', maxdown)
#            print(atrwindow, ' day ATR = ', tradedates['AverageTrueRangePoints'].loc[tradedates['RangeIndex'] == i][0])
            #MFE assignment
            MFEpoints = maxup
            MFElist.append(MFEpoints)
            #MFE assignment to trade dates            
#            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
            #MAE assignment
            MAEpoints = maxdown
            MAElist.append(MAEpoints)
            #MAE assignment to trade dates            
#            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown
        #For short trades
        if tradedates['OriginalTrade'].loc[tradedates['RangeIndex'] == i][0] == -1:
            if len(tempdf) < z-1 :
                MFElist.append(np.nan)
                MAElist.append(np.nan)
                print('Not enough data for this calculation')                
                continue
            print('Short entry at ', entryprice)             
            #Check status 
#            print(tempdf)
            #MAE
            maxup = max(tempdf['High'] - entryprice)
            #MFE       
            maxdown = max(entryprice - tempdf['Low'])  
            print('MFE in points = ', maxdown)            
            print('MAE in points = ', maxup)
#            print(atrwindow, ' day ATR = ', tradedates['AverageTrueRangePoints'].loc[tradedates['RangeIndex'] == i][0])
            #MFE assignment
            MFEpoints = maxdown
            MFElist.append(MFEpoints)
            #MFE assignment to trade dates                        
#            tradedates['MFEpoints'].loc[tradedates['RangeIndex'] == i] = maxdown
            #MAE assignment
            MAEpoints = maxup
            MAElist.append(MAEpoints)
            #MAE assignment to trade dates            
#            tradedates['MAEpoints'].loc[tradedates['RangeIndex'] == i] = maxup
#        print('--------------------------------------------')    
#        print('--------------------------------------------')    
#        print('--------------------------------------------')   
     
    #rotating column name
    nDay = str(z)

    print(MFElist)
    print(MAElist)   
    
    #To Series
    MFESeries = pd.Series(MFElist, index = tradedates.index)
    MAESeries = pd.Series(MAElist, index = tradedates.index)

    print(MFESeries)
    print(MAESeries)   
    
    #assign MFE/MAE to tradedates
    tradedates[nDay + 'DayMFE'] = MFESeries
    tradedates[nDay + 'DayMAE'] = MAESeries
    
    #clear lists
    MFElist = []
    MAElist = []
    
    #Adjust MFE and MAE for volatility - normalization
    tradedates[nDay + 'DayVolAdjMFE'] = tradedates[nDay + 'DayMFE']/tradedates['AverageTrueRangePoints']
    tradedates[nDay + 'DayVolAdjMAE'] = tradedates[nDay + 'DayMAE']/tradedates['AverageTrueRangePoints']
    #Add MFE and MAE values
    sumMFE = sum(tradedates[nDay + 'DayVolAdjMFE'].fillna(0))
    sumMAE = sum(tradedates[nDay + 'DayVolAdjMAE'].fillna(0))
    #Divide by number of signals
    AvgVolAdjMFE = sumMFE/numsignals
    AvgVolAdjMAE = sumMAE/numsignals 
        
    edgeratio = AvgVolAdjMFE/AvgVolAdjMAE
    
    print('The ', z, ' day edge ratio is', edgeratio)
    edgelist.append(edgeratio)
#              
#Length = len(Asset1['LogRet'])
#Range = range(0,Length)
#print(MaxDD*100, '% = Max Drawdown')
#
edgeratioframe = pd.DataFrame(index = range(2, len(edgelist) + 2))
edgeratioframe['EdgeRatio'] = edgelist
#
edgeratioframe['EdgeRatio'].plot(grid=True, figsize=(8,5))
#end = t.time()
#print((end - start), ' seconds later.')
#print('Max eRatio is', max(edgeratioframe['EdgeRatio']))

#Graphics
#X and Y axis scale figure
figure, axe = plt.subplots(figsize = (10,5))
#Assign axis labels
plt.ylabel(ticker + ' Price')
plt.xlabel('Date') 
#Overlay
axe.plot(AssetCopy['IndexToNumber'], Asset['RollingMax'], color = 'green', label = 'RollingMax')
axe.plot(AssetCopy['IndexToNumber'], Asset['RollingMin'], color = 'red', label = 'RollingMin')
#axe.plot(Asset['IndexToNumber'], Asset['SMA'], color = 'black', label = 'SMA')

#Signal triangles..
axe.scatter(Asset.loc[Asset['OriginalTrade'] == 1, 'IndexToNumber'].values, 
            Asset.loc[Asset['OriginalTrade'] == 1, 'EntryPrice'].values, label='skitscat', color='green', s=75, marker="^")
axe.scatter(Asset.loc[Asset['OriginalTrade'] == -1, 'IndexToNumber'].values, 
            Asset.loc[Asset['OriginalTrade'] == -1, 'EntryPrice'].values, label='skitscat', color='red', s=75, marker="v")

##Plot the DF values with the figure, object
candlestick_ohlc(axe, AssetCopy.values, width=.6, colorup='green', colordown='red')
axe.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

#For ATR
figure2, axe2 = plt.subplots(figsize = (10,2))
plt.ylabel(ticker + ' ATR Percent')
plt.xlabel('Date')
axe2.plot(AssetCopy['IndexToNumber'], Asset['AverageTrueRangePercent'], color = 'black', label = '4wkATRPercent')
#axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMax'], color = 'green', label = 'ATRRollingMax')
#axe2.plot(AssetCopy['IndexToNumber'], AssetCopy['ATRRollingMin'], color = 'red', label = 'ATRRollingMin')
axe2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))