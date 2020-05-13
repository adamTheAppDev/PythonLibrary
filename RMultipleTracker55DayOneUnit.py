# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Developed in Python 3.5

#This is a trading strategy model
#Does not function properly see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

#R Multiple Finder; Trade Tracking
#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Assign ticker
Ticker1 = 'VXX'
#Request data
Asset1 = YahooGrabber(Ticker1)

#Read in data ***ATTN*** insert path for OHLC data
#Asset1 = pd.read_pickle('C:\\Users\\Tasty\\Desktop\\WorkingDirectory\\UVXY')

#Declaration/Assignment
#Empty list
Empty = []
#Empty dataframe
Trades = pd.DataFrame()

#Timing statistics and iteration counter for optimization
#Start = t.time()
#Counter = 0
#start = t.time()

#The next 4 declarations are for use in fixed profit and loss based exits
#Exit stop loss - in percentages --------- however, looking to use ATR based stops
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
Asset1 = Asset1[:] #In

#Numbered subindex 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Assign variable windows
donchianwindow = 15
exitwindow = 13
ATRwindow = 20
stopwindow = 13
Counter = 0

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
#Calculate ATR
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()

#Market top and bottom calculation
Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
Asset1['RollingMin'] = Asset1['Low'].rolling(window=donchianwindow, center=False).min()
#Graphical display
#Asset1[['RollingMax','RollingMin','Adj Close']].plot()

#Signal = Price </> min/max
#If price is less than the min go long
#If price is greater than the max go short
Asset1['Signal'] = np.where(Asset1['High'] >= Asset1['RollingMax'].shift(1) , 1, 0)
Asset1['Signal'] = np.where(Asset1['Low'] <= Asset1['RollingMin'].shift(1) , -1, Asset1['Signal'])
#If Rolling Min/Max is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])

#To help identify "regime changes" i.e. last signal switches from short to long, vice versa
#Asset1['FilledSignal'] = np.where(Asset1['Signal'] == 0, np.nan, Asset1['Signal'] )
#Asset1['FilledSignal'] = Asset1['FilledSignal'].ffill(inplace = False)
#Asset1['FilledSignal'] = Asset1['FilledSignal'].fillna(0)

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
                              Asset1['RollingMax'].shift(1) + .01, np.nan)
#Long gap entry first unit
Asset1['EntryPriceUnitOne'].loc[(Asset1['Signal'] == 1) & (
            Asset1['Open'] > Asset1['EntryPriceUnitOne'])] = Asset1['Open']             
#Short entry first unit
Asset1['EntryPriceUnitOne'] = np.where(Asset1['Signal'] == -1, 
              Asset1['RollingMin'].shift(1) - .01, Asset1['EntryPriceUnitOne'])
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

#This is a profit target for long trades
Asset1['LimitExitPrice'] = np.where(Asset1['Signal'] == 1,
                 Asset1['EntryPriceUnitOne'] + (5 * Asset1['TradeATR']), np.nan)
#This is a profit target for short trades
Asset1['LimitExitPrice'] = np.where(Asset1['Signal'] == -1, 
    Asset1['EntryPriceUnitOne'] - (5 * Asset1['TradeATR']), Asset1['LimitExitPrice'])

#Begin loops for individual trade examination
#Iterable               
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

#1 = Short exit being hit starting the day of the signal. 
if TradeDirection == -1:
    TradeSubset['ShortExit'].loc[(TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])] = 1
if TradeDirection == 1:
#1 = Long exit being hit starting the day of the signal.
    TradeSubset['LongExit'].loc[(TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])] = 1

#Assess gaps on days where trade closes
TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
                TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1

TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
                 TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])] = 1

#Types of exit
TradeSubset['Exit'].loc[(TradeSubset['ShortExit'] == 1)] = 1 #1 indicating short exit
TradeSubset['Exit'].loc[(TradeSubset['LongExit'] == 1)] = 2 #1 indicating long exit 
TradeSubset['Exit'].loc[(TradeSubset['GapShortExit'] == 1)] = 3 #1 indicating short exit w/ gap
TradeSubset['Exit'].loc[(TradeSubset['GapLongExit'] == 1)] = 4 #1 indicating long exit w/ gap

while sum(abs(TradeSubset['Exit'])) != 0:
#while Counter < 1:
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
    #TradeDirection
    TradeDirection = TradeSubset['Signal'][0]

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
    
    #Price of gap open
    OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
    #Exit taken
    if ExitTaken == 1: # if exiting short trade, exit during market day
        TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 2: # if exiting long trade, exitduring market day 
        TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
    elif ExitTaken == 3: # if exiting short trade with gap 
        TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
    elif ExitTaken == 4: # if exiting long trade with gap 
        TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
    #Save trade details to list
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
    #Series to dataframe
    Trades[Counter] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
    #Trimmer trims the Trade out of the TradeSubset, then trims to the next signal
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
    #Exit price
    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
    ExitTaken = 0
    #Trade duration
    LengthOfTrade = len(TradeSubset)
    #Trade direction
    TradeDirection = TradeSubset['Signal'][0]
    #If long trade, calculate return
    if TradeDirection == 1:
        TradeReturn = (TradeSubset['HybridLongExitPrice'][-1] - EntryPriceUnitOne)/EntryPriceUnitOne
    #If short trade, calculate return
    elif TradeDirection == -1:
        TradeReturn = (EntryPriceUnitOne - TradeSubset['HybridLongExitPrice'][-1])/EntryPriceUnitOne
    #Exit date
    SubIndexOfEntry = TradeSubset['SubIndex'][0]
    SubIndexOfExit = np.nan    
    OpenPriceOnGap = np.nan
    #Save details to list
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
    Emptyseries = pd.Series(Empty)
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
#Calculate cumulative returns
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
