# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 09:04:55 2018

@author: AmatVictoriaCuramIII
"""
#Developed in Python 3.5

#R Multiple Finder; Trade Tracking
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Inputs - OHLC data
Ticker1 = 'UVXY'
Asset1 = YahooGrabber(Ticker1)

##Tasty OHLC; ***ATTN*** insert path for OHLC data
#Asset1 = pd.read_pickle('C:\\Users\\Tasty\\Desktop\\WorkingDirectory\\UVXY')

#Declaration/Assignments
#Empty list
Empty = []
#Empty dataframe
Trades = pd.DataFrame()

##Timing statistics and iteration counter for optimization
#Start = t.time()
#Counter = 0
#start = t.time()

##The next 4 declarations are for use in fixed profit and loss based exits
##Exit stop loss - in percentages --------- however, looking to use ATR based stops
#LongStopLoss = .005
#ShortStopLoss = .005
##Exit profit take -------- However, looking to use other exits, time based, trailing, ATR, etc.
#LongProfitTake = .01
#ShortProfitTake = .01

#Constraints in percentages
Commission = .01
Slippage = .01

#Time series trimmer for in/out sample data
#Asset1a = Asset1[-1250:] #Out
#Asset1 = Asset1[7:] #In
#
#Numbered subindex 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Variable windows
donchianwindow = 20
ATRwindow = 20
stopwindow = 13
Counter = 0
#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)



a = 12 #number of days for exp moving average window
b = 26 #numer of days for exp moving average window
c = 9 #number of days for exp moving average window for MACD line
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
multiplierC = (2/(c+1))
Range = range(0, len(Asset1['Adj Close']))
#Asset1['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
EMAyesterdayA = Asset1['Adj Close'][0] #these prices are based off the SMA values
EMAyesterdayB = Asset1['Adj Close'][0] #these prices are based off the SMA values
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (Asset1['Adj Close'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=Asset1.index)    
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (Asset1['Adj Close'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=Asset1.index)
Asset1['SmallEMA'] = smallEMAseries
Asset1['LargeEMA'] = largeEMAseries
Asset1['MACD'] = Asset1['SmallEMA'] - Asset1['LargeEMA']
MACDEMAyesterday = Asset1['MACD'][0]
MACDEMA = [MACDEMAyesterday]
for i in Range:
    holder2 = (Asset1['MACD'][i]*multiplierC) + (MACDEMAyesterday *
                                            (1-multiplierC))
    MACDEMA.append(holder2)
    MACDEMAyesterday = holder2
MACDEMAseries = pd.Series(MACDEMA[1:], index=Asset1.index)
Asset1['SignalLine'] = MACDEMAseries
Asset1['FlatLine'] = 0
#Asset1[['SmallEMA', 'LargeEMA', 'Close']].plot(grid=True, figsize=(8, 5))
#Asset1[['SignalLine','MACD','FlatLine']].plot(grid=True, figsize=(8, 3))

#ATR
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
#ATR in points; not %
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()

#Market top and bottom calculation
Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
Asset1['RollingMin'] = Asset1['Low'].rolling(window=donchianwindow, center=False).min()

#Asset1[['RollingMax','RollingMin','Close']].plot()

#Signal = Price </> min/max
#if MACD goes from - to + then long
#if MACD goes from + to - then short
Asset1['Signal'] = 0
Asset1['Signal'].loc[(Asset1['MACD'].shift(1) <= 0) & (Asset1['MACD'] > 0)] = 1
Asset1['Signal'].loc[(Asset1['MACD'].shift(1) > 0) & (Asset1['MACD'] <= 0)] = -1
#if Rolling Min/Max is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])

#Signal sub index numbers for segmenting data for trade analysis
SignalDates = Asset1['SubIndex'].loc[((Asset1['Signal'] != 0))]

#Trade ATR for signal
Asset1['TradeATR'] = np.where(Asset1['Signal'] != 0, Asset1['ATR'].shift(1), np.nan)
#experimental exits
Asset1['LimitExitPrice'] = np.nan
Asset1['ShortExitPrice'] =  Asset1['High'].rolling(window=stopwindow, center=False).max()
Asset1['LongExitPrice'] =  Asset1['Low'].rolling(window=stopwindow, center=False).min()

#Find the first trade of the signal period, so we can document entry prices
#Declare columns to record entry price and stop for unit one
Asset1['EntryPriceUnitOne'] = np.nan
Asset1['StopPriceUnitOne'] = np.nan
#Be sure to check for gaps on first unit entry and later on exits.
#Default stops and entries
#Long entry first unit
Asset1['EntryPriceUnitOne'] = np.where(Asset1['Signal'] == 1, 
                              Asset1['Adj Close'].shift(1) + .01, np.nan)
#Long gap entry first unit
Asset1['EntryPriceUnitOne'].loc[(Asset1['Signal'] == 1) & (
            Asset1['Open'] > Asset1['EntryPriceUnitOne'])] = Asset1['Open']             
#Short entry first unit
Asset1['EntryPriceUnitOne'] = np.where(Asset1['Signal'] == -1, 
              Asset1['Adj Close'].shift(1) - .01, Asset1['EntryPriceUnitOne'])
#Short gap entry first unit
Asset1['EntryPriceUnitOne'].loc[(Asset1['Signal'] == -1) & (
            Asset1['Open'] < Asset1['EntryPriceUnitOne'])] = Asset1['Open'] 
#Long stop first unit
Asset1['StopPriceUnitOne'] = np.where(Asset1['Signal'] == 1, 
                              Asset1['EntryPriceUnitOne'] - (Asset1['TradeATR'] * 2), np.nan)
#Short stop first unit
Asset1['StopPriceUnitOne'] = np.where(Asset1['Signal'] == -1, 
              Asset1['EntryPriceUnitOne'] + (Asset1['TradeATR'] * 2), Asset1['StopPriceUnitOne'])
              

#Experimental exits
Asset1['HybridShortExitPrice'] = np.where(Asset1['ShortExitPrice'] < Asset1['StopPriceUnitOne'],
                          Asset1['ShortExitPrice'], Asset1['StopPriceUnitOne'])  
Asset1['HybridLongExitPrice'] = np.where(Asset1['LongExitPrice'] > Asset1['StopPriceUnitOne'], 
                          Asset1['LongExitPrice'], Asset1['StopPriceUnitOne'])
Asset1['HybridShortExitPrice'] = Asset1['HybridShortExitPrice'].ffill()
Asset1['HybridLongExitPrice'] = Asset1['HybridLongExitPrice'].ffill()
#
##This is a profit target for long trades
#Asset1['LimitExitPrice'] = np.where(Asset1['Signal'] == 1,
#                 Asset1['EntryPriceUnitOne'] + (5 * Asset1['TradeATR']), np.nan)
##This is a profit target for short trades
#Asset1['LimitExitPrice'] = np.where(Asset1['Signal'] == -1, 
#    Asset1['EntryPriceUnitOne'] - (5 * Asset1['TradeATR']), Asset1['LimitExitPrice'])
#
#Begin loops for individual trade examination
#Novice indexing abilities               
TradeRanger = range(0,len(SignalDates))
#for r in TradeRanger:
TradeSubset = Asset1.loc[(Asset1['SubIndex'] >= SignalDates[0])] 
#TradeSubset = Asset1.loc[(Asset1['SubIndex'] >= 59) & (Asset1['SubIndex'] <= 87)] 
TradeDirection = TradeSubset['Signal'][0]
TradeSubset['Exit'] = 0
#
#Short exit, 1 = yes, 0 = no
TradeSubset['ShortExit'] = 0
#Long exit, 1 = yes, 0 = no
TradeSubset['LongExit'] = 0
#Did the exit gap overnight? or hit after open
TradeSubset['GapShortExit'] = 0
#Did the exit gap overnight? or hit after open
TradeSubset['GapLongExit'] = 0
#
#
# = Short exit being hit starting the day of the signal. 
if TradeDirection == -1:
    TradeSubset['ShortExit'].loc[(TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])] = 1
if TradeDirection == 1:
#1 = Long exit being hit starting the day of the signal.
    TradeSubset['LongExit'].loc[(TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])] = 1


#Assess Gaps on days where trade closes
TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
            TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1

TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
             TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])] = 1

#Types of exit
TradeSubset['Exit'].loc[(TradeSubset['ShortExit'] == 1)] = 1 #1 indicating short exit
TradeSubset['Exit'].loc[(TradeSubset['LongExit'] == 1)] = 2 #1 indicating long exit 
TradeSubset['Exit'].loc[(TradeSubset['GapShortExit'] == 1)] = 3 #1 indicating short exit w/ gap
TradeSubset['Exit'].loc[(TradeSubset['GapLongExit'] == 1)] = 4 #1 indicating long exit w/ gap



#List comprehension to find exit taken for subset.
#The next function gives a position on the TradeSubset index
ExitTaken = TradeSubset['Exit'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
#The length of the trade
LengthOfTrade = int(next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0))
#The SubIndex of the exit date is for continuing looking for rentry in new subset 
SubIndexOfEntry = TradeSubset['SubIndex'][0]
SubIndexOfExit = TradeSubset['SubIndex'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
TradeATR = TradeSubset['TradeATR'][0]
if TradeDirection == 1:
    StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
elif TradeDirection == -1:
    StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
if ExitTaken == 1: # if exiting short trade, exit during market day
    TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
elif ExitTaken == 2: # if exiting long trade, exitduring market day 
    TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
elif ExitTaken == 3: # if exiting short trade with gap 
    TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
elif ExitTaken == 4: # if exiting long trade with gap 
    TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
#Log Trade details in Trade dataframe
Empty.append(ExitTaken)
Empty.append(LengthOfTrade)
Empty.append(EntryPriceUnitOne)
Empty.append(StopPriceUnitOne)
Empty.append(SubIndexOfEntry)
Empty.append(SubIndexOfExit)
Empty.append(TradeDirection)
Empty.append(OpenPriceOnGap)
Empty.append(TradeReturn)
#Empty.append(RMultiple)
Emptyseries = pd.Series(Empty)
Trades[0] = Emptyseries.values
Empty[:] = [] 
#This trimmer trims the Trade out of the TradeSubset, then trims to the next signal!
TradeSubset = TradeSubset[(LengthOfTrade + 1):]
SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
TradeSubset = TradeSubset[SignalTrim:]
while sum(abs(TradeSubset['Exit'])) != 0:
#while Counter < 1:
    #TradeDirection
    TradeDirection = TradeSubset['Signal'][0]
    #I have to figure out how to add units..
    #TradeSubset['Units'] = 1
    #
    TradeSubset['Exit'] = 0
    #
    #Short exit, 1 = yes, 0 = no
    TradeSubset['ShortExit'] = 0
    #Long exit, 1 = yes, 0 = no
    TradeSubset['LongExit'] = 0
    #Did the exit gap overnight? or hit after open
    TradeSubset['GapShortExit'] = 0
    #Did the exit gap overnight? or hit after open
    TradeSubset['GapLongExit'] = 0
    
    #1 = Short exit being hit starting the day of the signal. 
    if TradeDirection == -1:
        TradeSubset['ShortExit'].loc[(TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])] = 1
    if TradeDirection == 1:
    #1 = Long exit being hit starting the day of the signal.
        TradeSubset['LongExit'].loc[(TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])] = 1
    
    
    #Assess Gaps on days where trade closes
    TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
                    TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1
    
    TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
                     TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])] = 1
    
    #Types of exit
    TradeSubset['Exit'].loc[(TradeSubset['ShortExit'] == 1)] = 1 #1 indicating short exit
    TradeSubset['Exit'].loc[(TradeSubset['LongExit'] == 1)] = 2 #1 indicating long exit 
    TradeSubset['Exit'].loc[(TradeSubset['GapShortExit'] == 1)] = 3 #1 indicating short exit w/ gap
    TradeSubset['Exit'].loc[(TradeSubset['GapLongExit'] == 1)] = 4 #1 indicating long exit w/ gap
    #
    #
    #List comprehension to find exit taken for subset.
    #The next function gives a position on the TradeSubset index
    ExitTaken = TradeSubset['Exit'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    #The length of the trade
    LengthOfTrade = int(next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0))
    #The SubIndex of the exit date is for continuing looking for rentry in new subset 
    SubIndexOfEntry = TradeSubset['SubIndex'][0]
    SubIndexOfExit = TradeSubset['SubIndex'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    TradeATR = TradeSubset['TradeATR'][0]
    OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    if TradeDirection == 1:
        StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    elif TradeDirection == -1:
        StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    if ExitTaken == 1: # if exiting short trade, exit during market day
        TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 2: # if exiting long trade, exitduring market day 
        TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 3: # if exiting short trade with gap 
        TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
    elif ExitTaken == 4: # if exiting long trade with gap 
        TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
    #Log Trade details in Trade dataframe
    Empty.append(ExitTaken)
    Empty.append(LengthOfTrade)
    Empty.append(EntryPriceUnitOne)
    Empty.append(StopPriceUnitOne)
    Empty.append(SubIndexOfEntry)
    Empty.append(SubIndexOfExit)
    Empty.append(TradeDirection)
    Empty.append(OpenPriceOnGap)
    Empty.append(TradeReturn)
    Empty.append(TradeATR)
    #Empty.append(RMultiple)
    Emptyseries = pd.Series(Empty)
    Trades[Counter] = Emptyseries.values
    Empty[:] = [] 
    #This trimmer trims the Trade out of the TradeSubset, then trims to the next signal!
    TradeSubset = TradeSubset[(LengthOfTrade + 1):]
    SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
    TradeSubset = TradeSubset[SignalTrim:]
#
    Counter = Counter + 1
    print(Counter)
    
#The last trade that is still open
if sum(abs(TradeSubset['Signal'])) != 0:
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
    ExitTaken = 0
    LengthOfTrade = len(TradeSubset)
    TradeDirection = TradeSubset['Signal'][0]
    if TradeDirection == 1:
        TradeReturn = (TradeSubset['HybridLongExitPrice'][-1] - EntryPriceUnitOne)/EntryPriceUnitOne
#            etc..
    elif TradeDirection == -1:
        TradeReturn = (EntryPriceUnitOne - TradeSubset['HybridLongExitPrice'][-1])/EntryPriceUnitOne

    SubIndexOfEntry = TradeSubset['SubIndex'][0]
    SubIndexOfExit = np.nan    
    OpenPriceOnGap = np.nan
    
    Empty.append(ExitTaken)
    Empty.append(LengthOfTrade)
    Empty.append(EntryPriceUnitOne)
    Empty.append(StopPriceUnitOne)
    Empty.append(SubIndexOfEntry)
    Empty.append(SubIndexOfExit)
    Empty.append(TradeDirection)
    Empty.append(OpenPriceOnGap)
    Empty.append(TradeReturn) 
    Emptyseries = pd.Series(Empty)
    Trades[Counter] = Emptyseries.values
    Empty[:] = [] 
    
    
Trades = Trades.rename(index={0: "ExitTaken", 1: "LengthOfTrade", 2: "EntryPriceUnitOne",
                3: "StopPriceUnitOne", 4: "SubIndexOfEntry", 5: "SubIndexOfExit",
                6: "TradeDirection", 7: "OpenPriceOnGap", 8: "TradeReturn"})
Asset1['Brackets'] = 1   
for d in Trades:
    Asset1['Brackets'].loc[(Asset1['SubIndex'] == Trades[d]['SubIndexOfExit'])] = 1 + Trades[d]['TradeReturn']
NumWinningTrades = len(Asset1['Brackets'][Asset1['Brackets'] > 1])
NumLosingTrades = len(Asset1['Brackets'][Asset1['Brackets'] < 1])
AvgWin = Asset1['Brackets'][Asset1['Brackets'] > 1].mean()
AvgLoss = Asset1['Brackets'][Asset1['Brackets'] < 1].mean()
RewardRisk = AvgWin/AvgLoss
WinRate = NumWinningTrades / (NumWinningTrades + NumLosingTrades)
LossRate = NumLosingTrades / (NumWinningTrades + NumLosingTrades)
Expectancy = (WinRate * RewardRisk) - (LossRate)

Asset1['Multiplier'] = Asset1['Brackets'].cumprod()
Asset1['Multiplier'].plot()
print(Expectancy)