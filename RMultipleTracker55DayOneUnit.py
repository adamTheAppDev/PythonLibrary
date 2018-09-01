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
Ticker1 = 'VXX'
Asset1 = YahooGrabber(Ticker1)
##Tasty OHLC; ***ATTN*** insert path for OHLC data
#Asset1 = pd.read_pickle('C:\\Users\\Tasty\\Desktop\\WorkingDirectory\\UVXY')

#Declaration/Assignment
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
Asset1 = Asset1[:] #In
#
#Numbered subindex 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Variable windows
donchianwindow = 15
exitwindow = 13
ATRwindow = 20
stopwindow = 13
Counter = 0
#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRwindow,
                                center=False).mean()

##Market top and bottom calculation
Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
Asset1['RollingMin'] = Asset1['Low'].rolling(window=donchianwindow, center=False).min()

#Asset1[['RollingMax','RollingMin','Adj Close']].plot()

##Signal = Price </> min/max
##if price is less than the min go long
##if price is greater than the max go short
Asset1['Signal'] = np.where(Asset1['High'] >= Asset1['RollingMax'].shift(1) , 1, 0)
Asset1['Signal'] = np.where(Asset1['Low'] <= Asset1['RollingMin'].shift(1) , -1, Asset1['Signal'])
#if Rolling Min/Max is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['RollingMax'] == np.nan, 0, Asset1['Signal'])

#To help identify "regime changes" i.e. last signal switches from short to long, vice versa
#Asset1['FilledSignal'] = np.where(Asset1['Signal'] == 0, np.nan, Asset1['Signal'] )
#Asset1['FilledSignal'] = Asset1['FilledSignal'].ffill(inplace = False)
#Asset1['FilledSignal'] = Asset1['FilledSignal'].fillna(0)

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

##Experimental exits
#TradeSubset['HybridShortExitPrice'] = np.where(TradeSubset['ShortExitPrice'] < TradeSubset['StopPriceUnitOne'],
#                          TradeSubset['ShortExitPrice'], TradeSubset['StopPriceUnitOne'])  
#TradeSubset['HybridLongExitPrice'] = np.where(TradeSubset['LongExitPrice'] > TradeSubset['StopPriceUnitOne'], 
#                          TradeSubset['LongExitPrice'], TradeSubset['StopPriceUnitOne'])
#TradeSubset['HybridShortExitPrice'] = TradeSubset['HybridShortExitPrice'].ffill()
#TradeSubset['HybridLongExitPrice'] = TradeSubset['HybridLongExitPrice'].ffill()
#
#
#
#
#
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
while sum(abs(TradeSubset['Exit'])) != 0:
#while Counter < 1:
    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
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
    
    ##Experimental exits
    #TradeSubset['HybridShortExitPrice'] = np.where(TradeSubset['ShortExitPrice'] < TradeSubset['StopPriceUnitOne'],
    #                          TradeSubset['ShortExitPrice'], TradeSubset['StopPriceUnitOne'])  
    #TradeSubset['HybridLongExitPrice'] = np.where(TradeSubset['LongExitPrice'] > TradeSubset['StopPriceUnitOne'], 
    #                          TradeSubset['LongExitPrice'], TradeSubset['StopPriceUnitOne'])
    #TradeSubset['HybridShortExitPrice'] = TradeSubset['HybridShortExitPrice'].ffill()
    #TradeSubset['HybridLongExitPrice'] = TradeSubset['HybridLongExitPrice'].ffill()
    #
    #
    #
    #
    #
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
#for a in Trades:
#    if Trades[a][8] == np.nan:
#        Trades = Trades.drop(a)
#In the event that we are stopped out, we want to continue to look for rentry.


#while sum(abs(TradeSubset['Signal'])) != 0:
#    EntryPriceUnitOne = TradeSubset['EntryPriceUnitOne'][0]
#    StopPriceUnitOne = TradeSubset['StopPriceUnitOne'][0]
#    
#    #I have to figure out how to add units..
#    TradeSubset['Units'] = 1
#    
#    TradeSubset['Exit'] = 0
#    
#    #Short exit, 1 = yes, 0 = no
#    TradeSubset['ShortExit'] = 0
#    #Long exit, 1 = yes, 0 = no
#    TradeSubset['LongExit'] = 0
#    #Did the exit gap overnight? or hit after open
#    TradeSubset['GapShortExit'] = 0
#    #Did the exit gap overnight? or hit after open
#    TradeSubset['GapLongExit'] = 0
#    
#    #1 = Short exit being hit starting the day of the signal. 
#    TradeSubset['ShortExit'].loc[(Asset1['FilledSignal'] == -1) & (
#                    TradeSubset['High'] > TradeSubset['HybridShortExitPrice'])] = 1    
#    #1 = Long exit being hit starting the day of the signal.
#    TradeSubset['LongExit'].loc[(Asset1['FilledSignal'] == 1) & (
#                      TradeSubset['Low'] < TradeSubset['HybridLongExitPrice'])] = 1
#    
#    
#    #Assess Gaps on days where trade closes
#    TradeSubset['GapShortExit'].loc[(TradeSubset['ShortExit'] == 1) & (
#                    TradeSubset['Open'] > TradeSubset['HybridShortExitPrice'])] = 1
#    
#    TradeSubset['GapLongExit'].loc[(TradeSubset['LongExit'] == 1) & (
#                     TradeSubset['Open'] < TradeSubset['HybridLongExitPrice'])] = 1
#    
#    #Types of exit
#    TradeSubset['Exit'].loc[(TradeSubset['ShortExit'] == 1)] = 1 #1 indicating short exit
#    TradeSubset['Exit'].loc[(TradeSubset['LongExit'] == 1)] = 2 #1 indicating long exit 
#    TradeSubset['Exit'].loc[(TradeSubset['GapShortExit'] == 1)] = 3 #1 indicating short exit w/ gap
#    TradeSubset['Exit'].loc[(TradeSubset['GapLongExit'] == 1)] = 4 #1 indicating long exit w/ gap
#    
#    #List comprehension to find exit taken for subset.
#    #The next function gives a position on the TradeSubset index
#    ExitTaken = TradeSubset['Exit'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
#    #The length of the trade
#    LengthOfTrade = int(next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0))
#    #The SubIndex of the exit date is for continuing looking for rentry in new subset 
#    SubIndexOfExit = TradeSubset['SubIndex'][next((n for n, x in enumerate(TradeSubset['Exit']) if x), 0)]
#    SubIndexOfEntry = TradeSubset['SubIndex'][0]
#    #TradeDirection
#    TradeDirection = TradeSubset['Signal'][0]
#    OpenPriceOnGap = TradeSubset['Open'][LengthOfTrade]
#    if ExitTaken == 1: # if exiting short trade, exit during market day
#        TradeReturn = (EntryPriceUnitOne - StopPriceUnitOne)/EntryPriceUnitOne
#    elif ExitTaken == 2: # if exiting long trade, exitduring market day 
#        TradeReturn = (StopPriceUnitOne - EntryPriceUnitOne)/EntryPriceUnitOne
#    elif ExitTaken == 3: # if exiting short trade with gap 
#        TradeReturn = (EntryPriceUnitOne - OpenPriceOnGap)/EntryPriceUnitOne
#    elif ExitTaken == 4: # if exiting long trade with gap 
#        TradeReturn = (OpenPriceOnGap - EntryPriceUnitOne)/EntryPriceUnitOne
#    
#    #In the event that we are stopped out, we want to continue to look for rentry.
#    TradeSubset = TradeSubset[(LengthOfTrade + 1):]


#Create individual trade subsets for examination
#TradeSubIndex = Asset1['SubIndex'].loc[(Asset1['OriginalSignal'] != 0)]
#TradeDates = pd.DataFrame()
#try:
#    for i in range(0, len(TradeSubIndex)):
#        TradeDates[i] = TradeSubIndex[i]-1,TradeSubIndex[i+1]
#except IndexError:
#    pass

#quick reference matrix for exits
#ExitReturns = pd.Series(index=range(0,10))
#ExitReturns[0] = 0
#ExitReturns[1] = 1 + LongProfitTake
#ExitReturns[2] = 1 + ShortProfitTake 
#ExitReturns[3] = 0
#ExitReturns[4] = 0
#ExitReturns[5] = 1 - LongStopLoss 
#ExitReturns[6] = 1 - ShortStopLoss 
#ExitReturns[7] = 1 - LongStopLoss
#ExitReturns[8] = 1 - ShortStopLoss
#ExitReturns[9] = 0
#ExitReturns[10] = 0
#Short, units added
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == -1) & (Asset1['Low'] < EntryPriceUnitTwo)] = 2
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == -1) & (Asset1['Low'] < EntryPriceUnitThree)] = 3
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == -1) & (Asset1['Low'] < EntryPriceUnitFour)] = 4
#Long, units added
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == 1) & (Asset1['High'] > EntryPriceUnitTwo)] = 2
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == 1) & (Asset1['High'] > EntryPriceUnitThree)] = 3
#TradeSubset['Units'].loc[(TradeSubset['FilledSignal'][0] == 1) & (Asset1['High'] > EntryPriceUnitFour)] = 4
#for l in range(0,len(TradeSubset['Units'])):
#    TradeSubset['Units'].loc[(TradeSubset['Units'] < TradeSubset['Units'].shift(1))] = TradeSubset['Units'].shift(1)  
#TradeSubset['Units'].loc[(TradeSubset['Units'] < TradeSubset['Units'].shift(1))] = TradeSubset['Units'].shift(1)  








##If it's the original signal, record entry price
#Asset1['EntryPrice'].loc[(Asset1['OriginalSignal'] != 0)] = Asset1['Adj Close']
#
##Assess spread/unfavorable fills here!
##Asset1['EntryPriceSlippage'] = Asset1['EntryPrice']
##Long slippage
##Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
##    Asset1['Signal'] == 1)] = Asset1['EntryPrice'] * (1 + Slippage) 
##Short slippage
##Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
##    Asset1['Signal'] == -1)] = Asset1['EntryPrice'] * (1 - Slippage)
##
##Run the entry price DOWN the column until new position is taken
##Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].ffill(inplace=False)
##Fill nan with 0 for entry price
##Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].fillna(0)
#
##Declare StopPrice column
#Asset1['StopPrice'] = np.nan
##Long stop calculation
#Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
#            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPrice'] * (1 - LongStopLoss)
##Short stop calculation
#Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
#            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPrice'] * (1 + ShortStopLoss)
##Forward fill
#Asset1['StopPrice'] = Asset1['StopPrice'].ffill(inplace=False)
#Asset1['StopPrice'] = Asset1['StopPrice'].fillna(0)
#
##Declare ProfitPrice column
#Asset1['ProfitPrice'] = np.nan
##Long stop calculation
#Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
#            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPrice'] * (1 + LongProfitTake)
##Short stop calculation
#Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
#            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPrice'] * (1 - ShortProfitTake)
##Forward fill
#Asset1['ProfitPrice'] = Asset1['ProfitPrice'].ffill(inplace=False)
#Asset1['ProfitPrice'] = Asset1['ProfitPrice'].fillna(0)
#
#Asset1['Exit'] = 0
##This will be the final return stream. Generally I use a regime of 
##(-1, or 0, or +1) multiplied by the next day's log return to get equity curve
#Asset1['BracketReturns'] = 1
#
##Short Take Gain exit, 1 = yes, 0 = no
#Asset1['STG'] = 0
##Short Take Gain exit, 1 = yes, 0 = no
#Asset1['SSL'] = 0
##Short Stop Loss exit, 1 = yes, 0 = no
#Asset1['LTG'] = 0
##Long Stop Loss exit, 1 = yes, 0 = no
#Asset1['LSL'] = 0
#
##For initial exits
#Asset1['OriginalSTG'] = 0
#Asset1['OriginalSSL'] = 0
#Asset1['OriginalLTG'] = 0
#Asset1['OriginalLSL'] = 0
#
#Asset1['GapSTG'] = 0
#Asset1['GapSSL'] = 0
#Asset1['GapLTG'] = 0
#Asset1['GapLSL'] = 0
#
##1 = STG being hit starting the day after the signal. After initial hit, 1s 
##will run down the column even though the trade should be closed
#Asset1['STG'].loc[(Asset1['Signal'] == -1) & (
#    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['ProfitPrice'])] = 1    
##find initial exit 
##Asset1['OriginalSTG'].loc[Asset1['STG'] != Asset1['STG'].shift(1)] = Asset1['STG']
#
#Asset1['LTG'].loc[(Asset1['Signal'] == 1) & (
#    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['ProfitPrice'])] = 1
##Asset1['OriginalLTG'].loc[Asset1['LTG'] != Asset1['LTG'].shift(1)] = Asset1['LTG']
#
#Asset1['SSL'].loc[(Asset1['Signal'] == -1) & (
#    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['StopPrice'])] = 1
##Asset1['OriginalSSL'].loc[Asset1['STG'] != Asset1['SSL'].shift(1)] = Asset1['SSL']
#
#Asset1['LSL'].loc[(Asset1['Signal'] == 1) & (
#    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['StopPrice'])] = 1
##Asset1['OriginalLSL'].loc[Asset1['LSL'] != Asset1['LSL'].shift(1)] = Asset1['LSL']
#
##Assess Gaps on days where trade closes
#Asset1['GapSTG'].loc[(Asset1['STG'] == 1) & (
#                      Asset1['Open'] < Asset1['ProfitPrice'])] = 1
#Asset1['GapSSL'].loc[(Asset1['SSL'] == 1) & (
#                      Asset1['Open'] > Asset1['StopPrice'])] = 1
#Asset1['GapLTG'].loc[(Asset1['LTG'] == 1) & (
#                      Asset1['Open'] > Asset1['ProfitPrice'])] = 1
#Asset1['GapLSL'].loc[(Asset1['LSL'] == 1) & (
#                      Asset1['Open'] < Asset1['StopPrice'])] = 1
#
##Days where StopPrice and ProfitPrice are both touched
#Asset1['LongDD'] = np.where((Asset1['LTG'] + Asset1['LSL']) == 2, 1, 0)
#Asset1['ShortDD'] = np.where((Asset1['STG'] + Asset1['SSL']) == 2, 1, 0)
#Asset1['DoubleDay'] = Asset1['LongDD'] + Asset1['ShortDD']
#
##Exit on DoubleDays - 1 & 2; LTG - 3; LSL - 4; STG - 5, SSL - 6.
##Preference given to stoploss on 'expensive' days
#Asset1['Exit'].loc[(Asset1['LTG'] == 1)] = 1 #exit as gain
#Asset1['Exit'].loc[(Asset1['STG'] == 1)] = 2 #exit as gain
#Asset1['Exit'].loc[(Asset1['GapSTG'] == 1)] = 3 #exit as gain
#Asset1['Exit'].loc[(Asset1['GapLTG'] == 1)] = 4 #exit as gain
#Asset1['Exit'].loc[(Asset1['LSL'] == 1)] = 5 #exit as loss
#Asset1['Exit'].loc[(Asset1['SSL'] == 1)] = 6 #exit as loss
#Asset1['Exit'].loc[(Asset1['LongDD'] == 1)] == 7 #exit long position at loss
#Asset1['Exit'].loc[(Asset1['ShortDD'] == 1)] == 8 #exit as short position at loss
#Asset1['Exit'].loc[(Asset1['GapSSL'] == 1)] = 9 #exit as loss
#Asset1['Exit'].loc[(Asset1['GapLSL'] == 1)] = 10 #exit as loss
#
##Create individual trade subsets for examination
#TradeSubIndex = Asset1['SubIndex'].loc[(Asset1['OriginalSignal'] != 0)]
#TradeDates = pd.DataFrame()
#try:
#    for i in range(0, len(TradeSubIndex)):
#        TradeDates[i] = TradeSubIndex[i]-1,TradeSubIndex[i+1]
#except IndexError:
#    pass
#
##quick reference matrix for exits
#ExitReturns = pd.Series(index=range(0,10))
#ExitReturns[0] = 0
#ExitReturns[1] = 1 + LongProfitTake
#ExitReturns[2] = 1 + ShortProfitTake 
#ExitReturns[3] = 0
#ExitReturns[4] = 0
#ExitReturns[5] = 1 - LongStopLoss 
#ExitReturns[6] = 1 - ShortStopLoss 
#ExitReturns[7] = 1 - LongStopLoss
#ExitReturns[8] = 1 - ShortStopLoss
#ExitReturns[9] = 0
#ExitReturns[10] = 0
#
##Trade Analysis from 0th trade
#for ii in TradeDates.columns:
#    TradeData = Asset1[TradeDates[ii][0]:TradeDates[ii][1]]
#    #the 'next' function yields index position of first non 0 exit
#    ExitTaken = TradeData['Exit'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
#    SubIndexOfExit = TradeData['SubIndex'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
#    TradeDuration = len(TradeData) - 1
#    TradeDirection = TradeData['Signal'][0]
#    TradeReturn = ExitReturns[ExitTaken]
#    RMultiple = (1 - TradeReturn)/ShortStopLoss
##If no stops are hit and there is a signal change, take P/L and switch position
#    if ExitTaken == 0:
#        SubIndexOfExit = TradeData['SubIndex'][-1]
#        if TradeDirection == 1:
#            TradeReturn = 1 + ((TradeData['Adj Close'][-1] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
#        elif TradeDirection == -1:
#            TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Adj Close'][-1])/TradeData['Adj Close'][0])
#    else:
#        pass
##Assess Gaps
#    #GAP STG
#    if ExitTaken == 3:
#        TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
#    else:
#        pass
#    #GAP LTG
#    if ExitTaken == 4:
#        TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
#    else:
#        pass
#    #GAP SSL
#    if ExitTaken == 9:
#        TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
#    else:
#        pass
#    #GAP LSL    
#    if ExitTaken == 10:
#        TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
#    else:
#        pass
#    RMultiple = (TradeReturn - 1)/ShortStopLoss
#    Empty.append(ExitTaken)
#    Empty.append(SubIndexOfExit)
#    Empty.append(TradeDuration)
#    Empty.append(TradeDirection)
#    Empty.append(TradeReturn)
#    Empty.append(RMultiple)
#    Emptyseries = pd.Series(Empty)
#    Dataset[ii] = Emptyseries.values
#    Empty[:] = [] 
##
#Dataset = Dataset.rename(index={0: "ExitTaken", 1: "SubIndex", 2: "TradeDuration",
#                                3: "TradeDirection", 4: "TradeReturn", 5: "RMultiple"})
#
#Asset1['Brackets'] = 1
#Asset1['SlippageCommissionBrackets'] = 1
#for d in Dataset:
#    Asset1['SlippageCommissionBrackets'].loc[(Asset1['SubIndex'] == Dataset[d]['SubIndex'])] = Dataset[d]['TradeReturn'] - Slippage - Commission
#for d in Dataset:
#    Asset1['Brackets'].loc[(Asset1['SubIndex'] == Dataset[d]['SubIndex'])] = Dataset[d]['TradeReturn']
#NumWinningTrades = len(Asset1['Brackets'][Asset1['Brackets'] > 1])
#NumLosingTrades = len(Asset1['Brackets'][Asset1['Brackets'] < 1])
#AvgWin = Asset1['Brackets'][Asset1['Brackets'] > 1].mean()
#AvgLoss = Asset1['Brackets'][Asset1['Brackets'] < 1].mean()
#RewardRisk = AvgWin/AvgLoss
#WinRate = NumWinningTrades / (NumWinningTrades + NumLosingTrades)
#LossRate = NumLosingTrades / (NumWinningTrades + NumLosingTrades)
#Expectancy = (WinRate * RewardRisk) - (LossRate)
#
#Asset1['Multiplier'] = Asset1['Brackets'].cumprod().plot()
#print(Expectancy)



#
##TradeData = Asset1[TradeDates[0][0]:TradeDates[0][1]]
###the 'next' function yields index position of first non 0 exit
##TradeData['ReIndex'] = range(0,len(TradeData))
##ExitTaken = TradeData['Exit'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
##SubIndexOfExit = TradeData['SubIndex'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
##TradeDuration = TradeData['ReIndex'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
##TradeDirection = TradeData['Signal'][0]
##TradeReturn = ExitReturns[ExitTaken]
##
###If no stops are hit and there is a signal change, take P/L and switch position
##if ExitTaken == 0:
##    SubIndexOfExit = TradeData['SubIndex'][-1]
##    if TradeDirection == 1:
##        TradeReturn = 1 + ((TradeData['Adj Close'][-1] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
##    elif TradeDirection == -1:
##        TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Adj Close'][-1])/TradeData['Adj Close'][0])
##else:
##    pass
###Assess Gaps
###GAP STG
##if ExitTaken == 3:
##    TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
##else:
##    pass
###GAP LTG
##if ExitTaken == 4:
##    TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
##else:
##    pass
###GAP SSL
##if ExitTaken == 9:
##    TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
##else:
##    pass
###GAP LSL    
##if ExitTaken == 10:
##    TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
##else:
##    pass
##Empty.append(ExitTaken)
##Empty.append(SubIndexOfExit)
##Empty.append(TradeDuration)
##Empty.append(TradeDirection)
##Empty.append(TradeReturn)
##Emptyseries = pd.Series(Empty)
###Dataset[ii] = Emptyseries.values
###Empty[:] = [] 
##print(Emptyseries)