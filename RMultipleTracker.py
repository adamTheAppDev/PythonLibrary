# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a trading strategy model
#Does not function properly see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

#R Multiple Documentation; Trade Tracking
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Empty lists used for optimization
Empty = []
somelist = []
#Empty Dataframes
Dataset = pd.DataFrame()
TradeSubIndex = pd.DataFrame()
Trades = pd.DataFrame()

#Timing statistics and iteration counter for optimization
#Start = t.time()
#Counter = 0

#Assign ticker
Ticker1 = 'SOYB'
#Request data
Asset1 = YahooGrabber(Ticker1)

#Variable assignment
LongStopLoss = .05
LongProfitTake = .3
ShortStopLoss = .05
ShortProfitTake = .3
Commission = .01
Slippage = .01

#Time series trimmer for in/out sample data
#Asset1a = Asset1[-1250:] #Out
Asset1 = Asset1[:] #In

#Numbered subindex
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#SMA window
window = 100

#SMA calculation
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()

#Current Close Price to SMA ratio
Asset1['Price/MA'] = Asset1['Adj Close']/Asset1['MA'].shift(1)

#Fill nan
Asset1['MA'] = Asset1['MA'].fillna(0)
Asset1['Price/MA'] = Asset1['Price/MA'].fillna(0)

#Signal = Price to Moving Average -- Directional methodology
#if price is greater than the MA go long w/ brackets
#if price is less than the MA go short w/ brackets
Asset1['Signal'] = np.where(Asset1['Price/MA'] >= 1, 1, -1)

#if MA is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['Price/MA'] == 0, 0, Asset1['Signal'])

#Find the first trade of the signal period and document entry price
Asset1['OriginalSignal'] = 0
Asset1['OriginalSignal'].loc[Asset1['Signal'] != Asset1['Signal'].shift(1)] = Asset1['Signal']
numsignals = sum(abs(Asset1['OriginalSignal']))

#Declare column to record entry price
Asset1['EntryPrice'] = np.nan

#If it's the original signal, record entry price
Asset1['EntryPrice'].loc[(Asset1['OriginalSignal'] != 0)] = Asset1['Adj Close']

#Assess spread/slippage on fills here
#Asset1['EntryPriceSlippage'] = Asset1['EntryPrice']
#Long slippage
#Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
#    Asset1['Signal'] == 1)] = Asset1['EntryPrice'] * (1 + Slippage) 
#Short slippage
#Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
#    Asset1['Signal'] == -1)] = Asset1['EntryPrice'] * (1 - Slippage)
#
#.ffill() entry price DOWN the column until new position is taken 
#Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].ffill(inplace=False)
#Fill nan with 0 for entry price
#Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].fillna(0)

#Declare StopPrice column
Asset1['StopPrice'] = np.nan
#Long stop calculation
Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPrice'] * (1 - LongStopLoss)
#Short stop calculation
Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPrice'] * (1 + ShortStopLoss)
#Forward fill
Asset1['StopPrice'] = Asset1['StopPrice'].ffill(inplace=False)
Asset1['StopPrice'] = Asset1['StopPrice'].fillna(0)

#Declare ProfitPrice column
Asset1['ProfitPrice'] = np.nan
#Long stop calculation
Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPrice'] * (1 + LongProfitTake)
#Short stop calculation
Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPrice'] * (1 - ShortProfitTake)
#Forward fill
Asset1['ProfitPrice'] = Asset1['ProfitPrice'].ffill(inplace=False)
Asset1['ProfitPrice'] = Asset1['ProfitPrice'].fillna(0)

#Zeros
Asset1['Exit'] = 0
#This will be the final return stream. Use a regime of 
#(-1, or 0, or +1) multiplied by the next day's log return to get equity curve
Asset1['BracketReturns'] = 1

#Short Take Gain exit, 1 = yes, 0 = no
Asset1['STG'] = 0
#Short Take Gain exit, 1 = yes, 0 = no
Asset1['SSL'] = 0
#Short Stop Loss exit, 1 = yes, 0 = no
Asset1['LTG'] = 0
#Long Stop Loss exit, 1 = yes, 0 = no
Asset1['LSL'] = 0

#For initial exits
Asset1['OriginalSTG'] = 0
Asset1['OriginalSSL'] = 0
Asset1['OriginalLTG'] = 0
Asset1['OriginalLSL'] = 0

Asset1['GapSTG'] = 0
Asset1['GapSSL'] = 0
Asset1['GapLTG'] = 0
Asset1['GapLSL'] = 0

#1 = STG being hit starting the day after the signal. After initial hit, 1s 
#will run down the column even though the trade should be closed
Asset1['STG'].loc[(Asset1['Signal'] == -1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['ProfitPrice'])] = 1    
#Find initial exit 
#Asset1['OriginalSTG'].loc[Asset1['STG'] != Asset1['STG'].shift(1)] = Asset1['STG']

Asset1['LTG'].loc[(Asset1['Signal'] == 1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['ProfitPrice'])] = 1
#Asset1['OriginalLTG'].loc[Asset1['LTG'] != Asset1['LTG'].shift(1)] = Asset1['LTG']

Asset1['SSL'].loc[(Asset1['Signal'] == -1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['StopPrice'])] = 1
#Asset1['OriginalSSL'].loc[Asset1['STG'] != Asset1['SSL'].shift(1)] = Asset1['SSL']

Asset1['LSL'].loc[(Asset1['Signal'] == 1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['StopPrice'])] = 1
#Asset1['OriginalLSL'].loc[Asset1['LSL'] != Asset1['LSL'].shift(1)] = Asset1['LSL']

#Assess Gaps on days where trade closes
Asset1['GapSTG'].loc[(Asset1['STG'] == 1) & (
                      Asset1['Open'] < Asset1['ProfitPrice'])] = 1
Asset1['GapSSL'].loc[(Asset1['SSL'] == 1) & (
                      Asset1['Open'] > Asset1['StopPrice'])] = 1
Asset1['GapLTG'].loc[(Asset1['LTG'] == 1) & (
                      Asset1['Open'] > Asset1['ProfitPrice'])] = 1
Asset1['GapLSL'].loc[(Asset1['LSL'] == 1) & (
                      Asset1['Open'] < Asset1['StopPrice'])] = 1

#Days where StopPrice and ProfitPrice are both touched
Asset1['LongDD'] = np.where((Asset1['LTG'] + Asset1['LSL']) == 2, 1, 0)
Asset1['ShortDD'] = np.where((Asset1['STG'] + Asset1['SSL']) == 2, 1, 0)
Asset1['DoubleDay'] = Asset1['LongDD'] + Asset1['ShortDD']

#Exit on DoubleDays - 1 & 2; LTG - 3; LSL - 4; STG - 5, SSL - 6.
#Preference given to stoploss on Double signal days
Asset1['Exit'].loc[(Asset1['LTG'] == 1)] = 1 #exit as gain
Asset1['Exit'].loc[(Asset1['STG'] == 1)] = 2 #exit as gain
Asset1['Exit'].loc[(Asset1['GapSTG'] == 1)] = 3 #exit as gain
Asset1['Exit'].loc[(Asset1['GapLTG'] == 1)] = 4 #exit as gain
Asset1['Exit'].loc[(Asset1['LSL'] == 1)] = 5 #exit as loss
Asset1['Exit'].loc[(Asset1['SSL'] == 1)] = 6 #exit as loss
Asset1['Exit'].loc[(Asset1['LongDD'] == 1)] == 7 #exit long position at loss
Asset1['Exit'].loc[(Asset1['ShortDD'] == 1)] == 8 #exit as short position at loss
Asset1['Exit'].loc[(Asset1['GapSSL'] == 1)] = 9 #exit as loss
Asset1['Exit'].loc[(Asset1['GapLSL'] == 1)] = 10 #exit as loss

#Create individual trade subsets for examination
TradeSubIndex = Asset1['SubIndex'].loc[(Asset1['OriginalSignal'] != 0)]
TradeDates = pd.DataFrame()
try:
    for i in range(0, len(TradeSubIndex)):
        TradeDates[i] = TradeSubIndex[i]-1,TradeSubIndex[i+1]
except IndexError:
    pass

#Reference matrix for exits
ExitReturns = pd.Series(index=range(0,10))
ExitReturns[0] = 0
ExitReturns[1] = 1 + LongProfitTake
ExitReturns[2] = 1 + ShortProfitTake 
ExitReturns[3] = 0
ExitReturns[4] = 0
ExitReturns[5] = 1 - LongStopLoss 
ExitReturns[6] = 1 - ShortStopLoss 
ExitReturns[7] = 1 - LongStopLoss
ExitReturns[8] = 1 - ShortStopLoss
ExitReturns[9] = 0
ExitReturns[10] = 0

#Trade Analysis from 0th trade
for ii in TradeDates.columns:
    TradeData = Asset1[TradeDates[ii][0]:TradeDates[ii][1]]
    #the 'next' function yields index position of first non 0 exit
    ExitTaken = TradeData['Exit'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
    SubIndexOfExit = TradeData['SubIndex'][next((n for n, x in enumerate(TradeData['Exit']) if x), 0)]
    TradeDuration = len(TradeData) - 1
    TradeDirection = TradeData['Signal'][0]
    TradeReturn = ExitReturns[ExitTaken]
#If no stops are hit and there is a signal change, take P/L and switch position
    if ExitTaken == 0:
        SubIndexOfExit = TradeData['SubIndex'][-1]
        if TradeDirection == 1:
            TradeReturn = 1 + ((TradeData['Adj Close'][-1] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
        elif TradeDirection == -1:
            TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Adj Close'][-1])/TradeData['Adj Close'][0])
    else:
        pass
#Assess Gaps
    #GAP STG
    if ExitTaken == 3:
        TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
    else:
        pass
    #GAP LTG
    if ExitTaken == 4:
        TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
    else:
        pass
    #GAP SSL
    if ExitTaken == 9:
        TradeReturn = 1 + ((TradeData['Adj Close'][0] - TradeData['Open'][TradeDuration])/TradeData['Adj Close'][0])
    else:
        pass
    #GAP LSL    
    if ExitTaken == 10:
        TradeReturn = 1 + ((TradeData['Open'][TradeDuration] - TradeData['Adj Close'][0])/TradeData['Adj Close'][0])
    else:
        pass
    #Save metrics to list
    Empty.append(ExitTaken)
    Empty.append(SubIndexOfExit)
    Empty.append(TradeDuration)
    Empty.append(TradeDirection)
    Empty.append(TradeReturn)
    #List to series 
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[ii] = Emptyseries.values
    Empty[:] = [] 
#Rename rows
Dataset = Dataset.rename(index={0: "ExitTaken", 1: "SubIndex", 2: "TradeDuration",
                                3: "TradeDirection", 4: "TradeReturn"})
#Ones
Asset1['Brackets'] = 1
Asset1['SlippageCommissionBrackets'] = 1
#Adding slippage and commission 
for d in Dataset:
    Asset1['SlippageCommissionBrackets'].loc[(Asset1['SubIndex'] == Dataset[d]['SubIndex'])] = Dataset[d]['TradeReturn'] - Slippage - Commission
#Define trade returns
for d in Dataset:
    Asset1['Brackets'].loc[(Asset1['SubIndex'] == Dataset[d]['SubIndex'])] = Dataset[d]['TradeReturn']
#Performance statistics
NumWinningTrades = len(Asset1['Brackets'][Asset1['Brackets'] > 1])
NumLosingTrades = len(Asset1['Brackets'][Asset1['Brackets'] < 1])
AvgWin = Asset1['Brackets'][Asset1['Brackets'] > 1].mean()
AvgLoss = Asset1['Brackets'][Asset1['Brackets'] < 1].mean()
RewardRisk = AvgWin/AvgLoss
WinRate = NumWinningTrades / (NumWinningTrades + NumLosingTrades)
LossRate = NumLosingTrades / (NumWinningTrades + NumLosingTrades)
Expectancy = (WinRate * RewardRisk) - (LossRate)
#Returns on $1
Asset1['Multiplier'] = Asset1['Brackets'].cumprod().plot()
#Display results
print(Expectancy)
#Graphical display
Asset1['Brackets'].plot()
