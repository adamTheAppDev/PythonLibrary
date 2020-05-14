# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Developed in Python 3.5

#This is a trading strategy model
#It looks like the stop logic and exit logic are correct
#also see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

#R Multiple Finder; Trade Tracking

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Assign ticker
Ticker1 = 'UVXY'
#Request data
Asset1 = YahooGrabber(Ticker1)

#Declaration/Assignments
#Empty list
Empty = []
#Empty dataframe
Trades = pd.DataFrame()

#Constraints in percentages
Commission = .01
Slippage = .01

#Time series trimmer for in/out sample data
#Asset1a = Asset1[-1250:] #Out
#Asset1 = Asset1[7:] #In

#Numbered subindex 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Variable windows
donchianwindow = 20
ATRwindow = 20
stopwindow = 13
Counter = 0

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Assign variables
a = 12 #number of days for exp moving average window
b = 26 #numer of days for exp moving average window
c = 9 #number of days for exp moving average window for MACD line
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
multiplierC = (2/(c+1))
#Iterable
Range = range(0, len(Asset1['Adj Close']))

#Initialize EMA values
EMAyesterdayA = Asset1['Adj Close'][0] #these prices are based off the SMA values
EMAyesterdayB = Asset1['Adj Close'][0] #these prices are based off the SMA values

#Calculate small EMA
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (Asset1['Adj Close'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=Asset1.index)

#Calculate large EMA
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (Asset1['Adj Close'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=Asset1.index)

#List to series
Asset1['SmallEMA'] = smallEMAseries
Asset1['LargeEMA'] = largeEMAseries
#Calculate MACD
Asset1['MACD'] = Asset1['SmallEMA'] - Asset1['LargeEMA']
#Inititalize MACD EMA
MACDEMAyesterday = Asset1['MACD'][0]
#Calculate MACD EMA
MACDEMA = [MACDEMAyesterday]
for i in Range:
    holder2 = (Asset1['MACD'][i]*multiplierC) + (MACDEMAyesterday *
                                            (1-multiplierC))
    MACDEMA.append(holder2)
    MACDEMAyesterday = holder2
MACDEMAseries = pd.Series(MACDEMA[1:], index=Asset1.index)
#MACD list to series
Asset1['SignalLine'] = MACDEMAseries

#Horizontal line
Asset1['FlatLine'] = 0

#Calculate ATR
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

#Zeros
Asset1['Signal'] = 0
#Signal = Price </> min/max
#If MACD goes from - to + then long
#If MACD goes from + to - then short
Asset1['Signal'].loc[(Asset1['MACD'].shift(1) <= 0) & (Asset1['MACD'] > 0)] = 1
Asset1['Signal'].loc[(Asset1['MACD'].shift(1) > 0) & (Asset1['MACD'] <= 0)] = -1
#If Rolling Min/Max is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])

#Signal sub index numbers for segmenting data for trade analysis
SignalDates = Asset1['SubIndex'].loc[((Asset1['Signal'] != 0))]

#Trade ATR for signal
Asset1['TradeATR'] = np.where(Asset1['Signal'] != 0, Asset1['ATR'].shift(1), np.nan)
#Experimental exits
Asset1['LimitExitPrice'] = np.nan
Asset1['ShortExitPrice'] =  Asset1['High'].rolling(window=stopwindow, center=False).max()
Asset1['LongExitPrice'] =  Asset1['Low'].rolling(window=stopwindow, center=False).min()

#Find the first trade of the signal period, document entry prices
#Declare columns to record entry price and stop for unit one
Asset1['EntryPriceUnitOne'] = np.nan
Asset1['StopPriceUnitOne'] = np.nan

#Check for gaps on first unit entry and later on exits.
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

#Iterable  
TradeRanger = range(0,len(SignalDates))
#Where the first trade begins - on first signal date
TradeSubset = Asset1.loc[(Asset1['SubIndex'] >= SignalDates[0])] 
#Trade direction
TradeDirection = TradeSubset['Signal'][0]
#Zeros
TradeSubset['Exit'] = 0

#Short exit, 1 = yes, 0 = no
TradeSubset['ShortExit'] = 0
#Long exit, 1 = yes, 0 = no
TradeSubset['LongExit'] = 0
#Did the exit gap overnight? or hit after open
TradeSubset['GapShortExit'] = 0
#Did the exit gap overnight? or hit after open
TradeSubset['GapLongExit'] = 0

#1 = Short exit being hit starting the day of the signal - if in short trade
if TradeDirection == -1:
    TradeSubset['ShortExit'].loc[(TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])] = 1
if TradeDirection == 1:
#1 = Long exit being hit starting the day of the signal - if in short trade
    TradeSubset['LongExit'].loc[(TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])] = 1

#Assess Gaps on days where short trade closes
TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
            TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1
#Assess Gaps on days where short trade closes
TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
             TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])] = 1

#Types of exits
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
#Entry price
EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
#ATR for trade
TradeATR = TradeSubset['TradeATR'][0]
#For long trade - get exit price
if TradeDirection == 1:
    StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
#For short trade - get exit price
elif TradeDirection == -1:
    StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
#Get open price for gap exits    
OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
#Exit types
if ExitTaken == 1: # if exiting short trade, exit during market day
    TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
elif ExitTaken == 2: # if exiting long trade, exitduring market day 
    TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
elif ExitTaken == 3: # if exiting short trade with gap 
    TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
elif ExitTaken == 4: # if exiting long trade with gap 
    TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
    
#Add metrics to list for first trade
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
#List to series
Emptyseries = pd.Series(Empty)
#Series to list
Trades[0] = Emptyseries.values
#Clear list
Empty[:] = [] 
#This trimmer trims the Trade out of the TradeSubset, then trims to the next signal!
TradeSubset = TradeSubset[(LengthOfTrade + 1):]
SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
TradeSubset = TradeSubset[SignalTrim:]

#While there are signals in time series
while sum(abs(TradeSubset['Exit'])) != 0:
#while Counter < 1:
    #TradeDirection
    TradeDirection = TradeSubset['Signal'][0]
    #Zeros
    TradeSubset['Exit'] = 0
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
    
    #Assess Gaps on days where trade closes for short trades
    TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
                    TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1
    #Assess Gaps on days where trade closes for long trades
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
    #ATR for trade
    TradeATR = TradeSubset['TradeATR'][0]
    #Open price for gap exit
    OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
    #Entry price
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    #Establish exit price for long trades
    if TradeDirection == 1:
        StopPriceUnitOne = TradeSubset['HybridLongExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
    #Establish exit price for short trades
    elif TradeDirection == -1:
        StopPriceUnitOne = TradeSubset['HybridShortExitPrice'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
        
    #Exit types    
    if ExitTaken == 1: # if exiting short trade, exit during market day
        TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 2: # if exiting long trade, exitduring market day 
        TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 3: # if exiting short trade with gap 
        TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
    elif ExitTaken == 4: # if exiting long trade with gap 
        TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
        
    #Add metrics to list
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
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Trades[Counter] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
    #This trimmer trims the Trade out of the TradeSubset, then trims to the next signal!
    TradeSubset = TradeSubset[(LengthOfTrade + 1):]
    SignalTrim = next((n for n, x in enumerate(TradeSubset['Signal']) if x), 0)
    TradeSubset = TradeSubset[SignalTrim:]
    #Iteration tracking
    Counter = Counter + 1
    print(Counter)
    
#The last trade that is still open
if sum(abs(TradeSubset['Signal'])) != 0:
    #Entry price
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    #Most recent price for exit price
    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
    #No exit taken
    ExitTaken = 0
    #Number of periods trade has been open
    LengthOfTrade = len(TradeSubset)
    #Trade direction
    TradeDirection = TradeSubset['Signal'][0]
    #Calculate returns for long trades 
    if TradeDirection == 1:
        TradeReturn = (TradeSubset['HybridLongExitPrice'][-1] - EntryPriceUnitOne)/EntryPriceUnitOne
    #Calculate returns for short trades
    elif TradeDirection == -1:
        TradeReturn = (EntryPriceUnitOne - TradeSubset['HybridLongExitPrice'][-1])/EntryPriceUnitOne
    #Entry date
    SubIndexOfEntry = TradeSubset['SubIndex'][0]
    #Trade is still open, no exit date
    SubIndexOfExit = np.nan    
    OpenPriceOnGap = np.nan
    #Add metrics to list
    Empty.append(ExitTaken)
    Empty.append(LengthOfTrade)
    Empty.append(EntryPriceUnitOne)
    Empty.append(StopPriceUnitOne)
    Empty.append(SubIndexOfEntry)
    Empty.append(SubIndexOfExit)
    Empty.append(TradeDirection)
    Empty.append(OpenPriceOnGap)
    Empty.append(TradeReturn) 
    #List to series
    Emptyseries = p.Series(Empty)
    #Series to dataframe
    Trades[Counter] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
    
#Rename rows
Trades = Trades.rename(index={0: "ExitTaken", 1: "LengthOfTrade", 2: "EntryPriceUnitOne",
                3: "StopPriceUnitOne", 4: "SubIndexOfEntry", 5: "SubIndexOfExit",
                6: "TradeDirection", 7: "OpenPriceOnGap", 8: "TradeReturn"})
#Ones
Asset1['Brackets'] = 1   
#Apply returns
for d in Trades:
    Asset1['Brackets'].loc[(Asset1['SubIndex'] == Trades[d]['SubIndexOfExit'])] = 1 + Trades[d]['TradeReturn']
    
#System statistics    
NumWinningTrades = len(Asset1['Brackets'][Asset1['Brackets'] > 1])
NumLosingTrades = len(Asset1['Brackets'][Asset1['Brackets'] < 1])
AvgWin = Asset1['Brackets'][Asset1['Brackets'] > 1].mean()
AvgLoss = Asset1['Brackets'][Asset1['Brackets'] < 1].mean()
RewardRisk = AvgWin/AvgLoss
WinRate = NumWinningTrades / (NumWinningTrades + NumLosingTrades)
LossRate = NumLosingTrades / (NumWinningTrades + NumLosingTrades)
Expectancy = (WinRate * RewardRisk) - (LossRate)
#Returns on $1
Asset1['Multiplier'] = Asset1['Brackets'].cumprod()
#Graphical display
Asset1['Multiplier'].plot()
#Display results
print(Expectancy)
