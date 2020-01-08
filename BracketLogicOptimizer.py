# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 01:20:06 2017

@author: AmatVictoriaCuramIII
"""

#This program is outdated and probably doesn't work
#See donchian trend models for properly functioning stop/profit taking/time based exits

#Bracket Logic w/ SMA Strategy

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Empty list used for 
Empty = []
#Empty Dataframes
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
#Timing statistics and iteration counter for optimization
Start = t.time()
Counter = 0
start = t.time()
iterations = range(0, 25000)

#Inputs - HLOC data
Ticker1 = 'UVXY'
Asset1 = YahooGrabber(Ticker1)
Asset1 = Asset1[-1000:]
#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
for i in iterations:
    a = rand.random() / 4
    b = rand.random() /4
    c = rand.randint(25,100)
    #In percentages
    LongStopLoss = a
    LongProfitTake = b
    ShortStopLoss = a
    ShortProfitTake = b
    Commission = .01
    Slippage = .01
    #Trimmer

    Counter = Counter + 1
    #SMA window
    window = c
    
    #SMA calculation
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
    
    #Current Close Price to SMA ratio
    Asset1['Price/MA'] = Asset1['Adj Close']/Asset1['MA']
    
    #Fill nan
    Asset1['MA'] = Asset1['MA'].fillna(0)
    Asset1['Price/MA'] = Asset1['Price/MA'].fillna(0)
    
    #Signal, if price is greater than the MA go long w/ brackets
    #if price is less than the MA go short w/ brackets
    Asset1['Signal'] = np.where(Asset1['Price/MA'] >= 1, 1, -1)
    
    #if MA is still being computed, stay out of market
    Asset1['Signal'] = np.where(Asset1['Price/MA'] == 0, 0, Asset1['Signal'])
    
    #Find the first trade of the signal period, so we can document entry price
    Asset1['OriginalSignal'] = 0
    Asset1['OriginalSignal'].loc[Asset1['Signal'] != Asset1['Signal'].shift(1)] = Asset1['Signal']
    numtrades = sum(abs(Asset1['OriginalSignal']))
    if numtrades < 60:
        continue
    #Declare column to record entry price
    Asset1['EntryPrice'] = np.nan
    
    #If it's the original signal, record entry price
    Asset1['EntryPrice'].loc[(Asset1['OriginalSignal'] != 0)] = Asset1['Adj Close']
    
    #Assess price slippage here!
    Asset1['EntryPriceSlippage'] = Asset1['EntryPrice']
    #Long slippage
    Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
        Asset1['Signal'] == 1)] = Asset1['EntryPrice'] * (1 + Slippage) 
    #Short slippage
    Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
        Asset1['Signal'] == -1)] = Asset1['EntryPrice'] * (1 - Slippage)
    
    #Run the entry price DOWN the column until new position is taken
    Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].ffill(inplace=False)
    #Fill nan with 0 for entry price
    Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].fillna(0)
    
    #Declare StopPrice column
    Asset1['StopPrice'] = np.nan
    #Long stop calculation
    Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
                Asset1['OriginalSignal'] == 1)] = Asset1['EntryPriceSlippage'] * (1 - LongStopLoss)
    #Short stop calculation
    Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
                Asset1['OriginalSignal'] == -1)] = Asset1['EntryPriceSlippage'] * (1 + ShortStopLoss)
    #Forward fill
    Asset1['StopPrice'] = Asset1['StopPrice'].ffill(inplace=False)
    Asset1['StopPrice'] = Asset1['StopPrice'].fillna(0)
    
    #Declare ProfitPrice column
    Asset1['ProfitPrice'] = np.nan
    #Long stop calculation
    Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
                Asset1['OriginalSignal'] == 1)] = Asset1['EntryPriceSlippage'] * (1 + LongProfitTake)
    #Short stop calculation
    Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
                Asset1['OriginalSignal'] == -1)] = Asset1['EntryPriceSlippage'] * (1 - ShortProfitTake)
    #Forward fill
    Asset1['ProfitPrice'] = Asset1['ProfitPrice'].ffill(inplace=False)
    Asset1['ProfitPrice'] = Asset1['ProfitPrice'].fillna(0)
    
    #MFE, MAE are used to calculate 'edge ratio'. May be useful for further strategy analysis
    #Declare - Max Favorable Excursion (favorable price movement from entry)
#    Asset1['MFE'] = 0
#    
#    #Declare - Max Adverse Excursion (adverse price movement from entry)
#    Asset1['MAE'] = 0
#    
#    #MFE for long positions, MAE for short positions. Based on direction, entry price, daily high, and daily low
#    Asset1['LongGains'] = (Asset1['High'] - Asset1['EntryPrice'].shift(1))/Asset1['EntryPrice'].shift(1)
#    Asset1['LongGains'] = Asset1['LongGains'].replace([np.inf, -np.inf], np.nan)
#    Asset1['LongGains'] = Asset1['LongGains'].fillna(0)
#    #MAE for long positions, MFE for short positions. Based on direction, entry price, daily high, and daily low
#    Asset1['ShortGains'] = (Asset1['EntryPrice'].shift(1) - Asset1['Low'])/Asset1['EntryPrice'].shift(1)
#    Asset1['ShortGains'] = Asset1['ShortGains'].replace([np.inf, -np.inf], np.nan)
#    Asset1['ShortGains'] = Asset1['ShortGains'].fillna(0)
    
    #We have to exit the trade... 
    #Redundant column assignment
    Asset1['Exit'] = 0
    Asset1['BracketReturns'] = 1
    Asset1['STG'] = 0
    Asset1['SSL'] = 0
    Asset1['LTG'] = 0
    Asset1['LSL'] = 0
    Asset1['DD'] = 0
    
    Asset1['OriginalSTG'] = 0
    Asset1['OriginalSSL'] = 0
    Asset1['OriginalLTG'] = 0
    Asset1['OriginalLSL'] = 0
    
    Asset1['GapSTG'] = 0
    Asset1['GapSSL'] = 0
    Asset1['GapLTG'] = 0
    Asset1['GapLSL'] = 0
    
    #Short Take Gain starting day after signal = 1
    Asset1['STG'].loc[(Asset1['Signal'] == -1) & (
        Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['ProfitPrice'])] = 1    
    Asset1['OriginalSTG'].loc[Asset1['STG'] != Asset1['STG'].shift(1)] = Asset1['STG']
    #Long Take Gain starting day after signal = 1
    Asset1['LTG'].loc[(Asset1['Signal'] == 1) & (
        Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['ProfitPrice'])] = 1
    Asset1['OriginalLTG'].loc[Asset1['LTG'] != Asset1['LTG'].shift(1)] = Asset1['LTG']
    #Short Stop Loss starting day after signal = 1
    Asset1['SSL'].loc[(Asset1['Signal'] == -1) & (
        Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['StopPrice'])] = 1
    Asset1['OriginalSSL'].loc[Asset1['STG'] != Asset1['SSL'].shift(1)] = Asset1['SSL']
    #Long Stop loss starting day after signal = 1
    Asset1['LSL'].loc[(Asset1['Signal'] == 1) & (
        Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['StopPrice'])] = 1
    Asset1['OriginalLSL'].loc[Asset1['LSL'] != Asset1['LSL'].shift(1)] = Asset1['LSL']
    
    #Asses Gaps on days where trade closes
    Asset1['GapSTG'].loc[(Asset1['OriginalSTG'] == 1) & (
                          Asset1['Open'] < Asset1['ProfitPrice'])] = 1
    Asset1['GapSSL'].loc[(Asset1['OriginalSSL'] == 1) & (
                          Asset1['Open'] > Asset1['StopPrice'])] = 1
    Asset1['GapLTG'].loc[(Asset1['OriginalLTG'] == 1) & (
                          Asset1['Open'] > Asset1['ProfitPrice'])] = 1
    Asset1['GapLSL'].loc[(Asset1['OriginalLSL'] == 1) & (
                          Asset1['Open'] < Asset1['StopPrice'])] = 1
    
    #Days where StopPrice and ProfitPrice are both touched
    Asset1['LongDD'] = np.where((Asset1['LTG'] + Asset1['LSL']) == 2, 1, 0)
    Asset1['ShortDD'] = np.where((Asset1['STG'] + Asset1['SSL']) == 2, 1, 0)
    Asset1['DoubleDay'] = Asset1['LongDD'] + Asset1['ShortDD']
    
    #Exit on DoubleDays - 1; LTG - 2; LSL - 3; STG - 4, SSL - 5.
    #Preference given to losses on 'double days'
    Asset1['Exit'].loc[(Asset1['LongDD'] == 1)] == 1 #exit long position at loss
    Asset1['Exit'].loc[(Asset1['ShortDD'] == 1)] == 2 #exit as short position at loss
    Asset1['Exit'].loc[(Asset1['OriginalLTG'] == 1)] = 3 #exit as gain
    Asset1['Exit'].loc[(Asset1['OriginalLSL'] == 1)] = 4 #exit as loss
    Asset1['Exit'].loc[(Asset1['OriginalSTG'] == 1)] = 5 #exit as gain
    Asset1['Exit'].loc[(Asset1['OriginalSSL'] == 1)] = 6 #exit as loss
    
    #Bring the brackets to life
    #Assess Commissions on close of trade
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 1)] = (1 - LongStopLoss) - Commission
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 2)] = 1 - ShortStopLoss - Commission
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 3)] = 1 + LongProfitTake - Commission
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 4)] = 1 - LongStopLoss - Commission
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 5)] = 1 + ShortProfitTake - Commission
    Asset1['BracketReturns'].loc[(Asset1['Exit'] == 6)] = 1 - ShortStopLoss - Commission
    Asset1['BracketReturns'].loc[(Asset1['GapSTG'] == 1)] = 1 + ((
        Asset1['EntryPriceSlippage'] - Asset1['Open'])/Asset1['EntryPriceSlippage'])
    Asset1['BracketReturns'].loc[(Asset1['GapSSL'] == 1)] = 1 + ((
        Asset1['EntryPriceSlippage'] - Asset1['Open'])/Asset1['EntryPriceSlippage'])
    Asset1['BracketReturns'].loc[(Asset1['GapLTG'] == 1)] = 1 + ((
        Asset1['Open'] - Asset1['EntryPriceSlippage'])/Asset1['EntryPriceSlippage'])
    Asset1['BracketReturns'].loc[(Asset1['GapLSL'] == 1)] = 1 + ((
        Asset1['Open'] - Asset1['EntryPriceSlippage'])/Asset1['EntryPriceSlippage'])
    
    #Eliminate exits for flat days; There are no flat signals after the first trade, thus 
    #no calculation for trading days where a position is held on open, but close signal is flat    
    #Asset1['Exit'].loc[(Asset1['Signal'] == 0)] = 0
    
    Asset1['Multiplier'] = Asset1['BracketReturns'].cumprod()
#    Asset1['Multiplier'].plot() 
    #Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['NewSignal'].shift(1))
    #Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #
    dailyreturn = (Asset1['BracketReturns'] - 1).mean()
    ##
    #Dailyvol is going to be inaccurate because account equity is not calculated during holding period, only assessed on exit 
    dailyvol = (Asset1['BracketReturns'] - 1).std()
    sharpe =(dailyreturn/dailyvol)
    print(Counter)
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 

z1 = Dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])

LongStopLoss = Dataset[kfloat][0]
LongProfitTake = Dataset[kfloat][1]
ShortStopLoss = Dataset[kfloat][0]
ShortProfitTake = Dataset[kfloat][1]
Commission = .01
Slippage = .01
#Trimmer
#Asset1 = Asset1[-600:]
#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#SMA window
window = int(Dataset[kfloat][2])

#SMA calculation
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()

#Current Close Price to SMA ratio
Asset1['Price/MA'] = Asset1['Adj Close']/Asset1['MA']

#Fill nan
Asset1['MA'] = Asset1['MA'].fillna(0)
Asset1['Price/MA'] = Asset1['Price/MA'].fillna(0)

#Signal, if price is greater than the MA go long w/ brackets
#if price is less than the MA go short w/ brackets
Asset1['Signal'] = np.where(Asset1['Price/MA'] >= 1, 1, -1)

#if MA is still being computed, stay out of market
Asset1['Signal'] = np.where(Asset1['Price/MA'] == 0, 0, Asset1['Signal'])

#Find the first trade of the signal period, so we can document entry price
Asset1['OriginalSignal'] = 0
Asset1['OriginalSignal'].loc[Asset1['Signal'] != Asset1['Signal'].shift(1)] = Asset1['Signal']
numtrades = sum(abs(Asset1['OriginalSignal']))
#Declare column to record entry price
Asset1['EntryPrice'] = np.nan

#If it's the original signal, record entry price
Asset1['EntryPrice'].loc[(Asset1['OriginalSignal'] != 0)] = Asset1['Adj Close']

#Assess price slippage here!
Asset1['EntryPriceSlippage'] = Asset1['EntryPrice']
#Long slippage
Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
    Asset1['Signal'] == 1)] = Asset1['EntryPrice'] * (1 + Slippage) 
#Short slippage
Asset1['EntryPriceSlippage'].loc[(Asset1['EntryPrice'] != 0) & (
    Asset1['Signal'] == -1)] = Asset1['EntryPrice'] * (1 - Slippage)

#Run the entry price DOWN the column until new position is taken
Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].ffill(inplace=False)
#Fill nan with 0 for entry price
Asset1['EntryPriceSlippage'] = Asset1['EntryPriceSlippage'].fillna(0)

#Declare StopPrice column
Asset1['StopPrice'] = np.nan
#Long stop calculation
Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPriceSlippage'] * (1 - LongStopLoss)
#Short stop calculation
Asset1['StopPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPriceSlippage'] * (1 + ShortStopLoss)
#Forward fill
Asset1['StopPrice'] = Asset1['StopPrice'].ffill(inplace=False)
Asset1['StopPrice'] = Asset1['StopPrice'].fillna(0)

#Declare ProfitPrice column
Asset1['ProfitPrice'] = np.nan
#Long stop calculation
Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == 1)] = Asset1['EntryPriceSlippage'] * (1 + LongProfitTake)
#Short stop calculation
Asset1['ProfitPrice'].loc[(Asset1['EntryPrice'] != 0) & (
            Asset1['OriginalSignal'] == -1)] = Asset1['EntryPriceSlippage'] * (1 - ShortProfitTake)
#Forward fill
Asset1['ProfitPrice'] = Asset1['ProfitPrice'].ffill(inplace=False)
Asset1['ProfitPrice'] = Asset1['ProfitPrice'].fillna(0)

#MFE, MAE are used to calculate 'edge ratio'. May be useful for further strategy analysis
#Declare - Max Favorable Excursion (favorable price movement from entry)
Asset1['MFE'] = 0

#Declare - Max Adverse Excursion (adverse price movement from entry)
Asset1['MAE'] = 0

#MFE for long positions, MAE for short positions. Based on direction, entry price, daily high, and daily low
Asset1['LongGains'] = (Asset1['High'] - Asset1['EntryPrice'].shift(1))/Asset1['EntryPrice'].shift(1)
Asset1['LongGains'] = Asset1['LongGains'].replace([np.inf, -np.inf], np.nan)
Asset1['LongGains'] = Asset1['LongGains'].fillna(0)
#MAE for long positions, MFE for short positions. Based on direction, entry price, daily high, and daily low
Asset1['ShortGains'] = (Asset1['EntryPrice'].shift(1) - Asset1['Low'])/Asset1['EntryPrice'].shift(1)
Asset1['ShortGains'] = Asset1['ShortGains'].replace([np.inf, -np.inf], np.nan)
Asset1['ShortGains'] = Asset1['ShortGains'].fillna(0)

#We have to exit the trade... 
#Redundant column assignment
Asset1['Exit'] = 0
Asset1['BracketReturns'] = 1
Asset1['STG'] = 0
Asset1['SSL'] = 0
Asset1['LTG'] = 0
Asset1['LSL'] = 0
Asset1['DD'] = 0

Asset1['OriginalSTG'] = 0
Asset1['OriginalSSL'] = 0
Asset1['OriginalLTG'] = 0
Asset1['OriginalLSL'] = 0

Asset1['GapSTG'] = 0
Asset1['GapSSL'] = 0
Asset1['GapLTG'] = 0
Asset1['GapLSL'] = 0

#Short Take Gain starting day after signal = 1
Asset1['STG'].loc[(Asset1['Signal'] == -1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['ProfitPrice'])] = 1    
Asset1['OriginalSTG'].loc[Asset1['STG'] != Asset1['STG'].shift(1)] = Asset1['STG']
#Long Take Gain starting day after signal = 1
Asset1['LTG'].loc[(Asset1['Signal'] == 1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['ProfitPrice'])] = 1
Asset1['OriginalLTG'].loc[Asset1['LTG'] != Asset1['LTG'].shift(1)] = Asset1['LTG']
#Short Stop Loss starting day after signal = 1
Asset1['SSL'].loc[(Asset1['Signal'] == -1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['High'] > Asset1['StopPrice'])] = 1
Asset1['OriginalSSL'].loc[Asset1['STG'] != Asset1['SSL'].shift(1)] = Asset1['SSL']
#Long Stop loss starting day after signal = 1
Asset1['LSL'].loc[(Asset1['Signal'] == 1) & (
    Asset1['OriginalSignal'] == 0) & (Asset1['Low'] < Asset1['StopPrice'])] = 1
Asset1['OriginalLSL'].loc[Asset1['LSL'] != Asset1['LSL'].shift(1)] = Asset1['LSL']

#Asses Gaps on days where trade closes
Asset1['GapSTG'].loc[(Asset1['OriginalSTG'] == 1) & (
                      Asset1['Open'] < Asset1['ProfitPrice'])] = 1
Asset1['GapSSL'].loc[(Asset1['OriginalSSL'] == 1) & (
                      Asset1['Open'] > Asset1['StopPrice'])] = 1
Asset1['GapLTG'].loc[(Asset1['OriginalLTG'] == 1) & (
                      Asset1['Open'] > Asset1['ProfitPrice'])] = 1
Asset1['GapLSL'].loc[(Asset1['OriginalLSL'] == 1) & (
                      Asset1['Open'] < Asset1['StopPrice'])] = 1

#Days where StopPrice and ProfitPrice are both touched
Asset1['LongDD'] = np.where((Asset1['LTG'] + Asset1['LSL']) == 2, 1, 0)
Asset1['ShortDD'] = np.where((Asset1['STG'] + Asset1['SSL']) == 2, 1, 0)
Asset1['DoubleDay'] = Asset1['LongDD'] + Asset1['ShortDD']

#Exit on DoubleDays - 1; LTG - 2; LSL - 3; STG - 4, SSL - 5.
#Preference given to losses on 'double days'
Asset1['Exit'].loc[(Asset1['LongDD'] == 1)] == 1 #exit long position at loss
Asset1['Exit'].loc[(Asset1['ShortDD'] == 1)] == 2 #exit as short position at loss
Asset1['Exit'].loc[(Asset1['OriginalLTG'] == 1)] = 3 #exit as gain
Asset1['Exit'].loc[(Asset1['OriginalLSL'] == 1)] = 4 #exit as loss
Asset1['Exit'].loc[(Asset1['OriginalSTG'] == 1)] = 5 #exit as gain
Asset1['Exit'].loc[(Asset1['OriginalSSL'] == 1)] = 6 #exit as loss

#Bring the brackets to life
#Assess Commissions on close of trade
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 1)] = (1 - LongStopLoss) - Commission
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 2)] = 1 - ShortStopLoss - Commission
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 3)] = 1 + LongProfitTake - Commission
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 4)] = 1 - LongStopLoss - Commission
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 5)] = 1 + ShortProfitTake - Commission
Asset1['BracketReturns'].loc[(Asset1['Exit'] == 6)] = 1 - ShortStopLoss - Commission
Asset1['BracketReturns'].loc[(Asset1['GapSTG'] == 1)] = 1 + ((
    Asset1['EntryPriceSlippage'] - Asset1['Open'])/Asset1['EntryPriceSlippage'])
Asset1['BracketReturns'].loc[(Asset1['GapSSL'] == 1)] = 1 + ((
    Asset1['EntryPriceSlippage'] - Asset1['Open'])/Asset1['EntryPriceSlippage'])
Asset1['BracketReturns'].loc[(Asset1['GapLTG'] == 1)] = 1 + ((
    Asset1['Open'] - Asset1['EntryPriceSlippage'])/Asset1['EntryPriceSlippage'])
Asset1['BracketReturns'].loc[(Asset1['GapLSL'] == 1)] = 1 + ((
    Asset1['Open'] - Asset1['EntryPriceSlippage'])/Asset1['EntryPriceSlippage'])

#Eliminate exits for flat days; There are no flat signals after the first trade, thus 
#no calculation for trading days where a position is held on open, but close signal is flat    
#Asset1['Exit'].loc[(Asset1['Signal'] == 0)] = 0

Asset1['Multiplier'] = Asset1['BracketReturns'].cumprod()
Asset1['Multiplier'].plot() 
#Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['NewSignal'].shift(1))
#Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
MaxDD = max(drawdown)
#
dailyreturn = (Asset1['BracketReturns'] - 1).mean()
##
#Dailyvol is going to be inaccurate because account equity is not calculated during holding period, only assessed on exit 
dailyvol = (Asset1['BracketReturns'] - 1).std()
sharpe =(dailyreturn/dailyvol)

#Portfolio['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#Portfolio['Multiplier'] = Portfolio['Multiplier'].fillna(1)
#drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#MaxDD = max(drawdown)
#print(MaxDD)
##end = t.time()
##totaltime = end - start
##print('Time taken = ', totaltime)
#Portfolio['Multiplier'].plot()
