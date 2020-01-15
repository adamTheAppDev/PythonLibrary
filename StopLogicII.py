# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 01:20:06 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester for the implementation of stop logic - looks under construction
#It probably doesn't work properly, see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

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

#Inputs - HLOC data
Ticker1 = 'UVXY'
Asset1 = YahooGrabber(Ticker1)

#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#SMA window
window = 15

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

#Declare column to record entry price
Asset1['EntryPrice'] = 0

#If it's the original signal, record entry price
Asset1['EntryPrice'].loc[Asset1['OriginalSignal'] != 0] = Asset1['Adj Close']

#Help needed here
#All I'm trying to do is just run the entry price DOWN the column until new position is taken
for i in range(0,35):
    Asset1['EntryPrice'].loc[Asset1['OriginalSignal'] == 0] = Asset1['EntryPrice'].shift(1)

#Fill nan with 0 for entry price
Asset1['EntryPrice'] = Asset1['EntryPrice'].fillna(0)

#Max Favorable Excursion (favorable price movement from entry)
Asset1['MFE'] = 0

#Max Adverse Excursion (adverse price movement from entry)
Asset1['MAE'] = 0


Asset1['LongGains'] = (Asset1['High'] - Asset1['EntryPrice'].shift(1))/Asset1['EntryPrice'].shift(1)
Asset1['ShortGains'] = (Asset1['EntryPrice'].shift(1) - Asset1['Low'])/Asset1['EntryPrice'].shift(1)
#
#
#Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Signal'].shift(1))
#Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
#MaxDD = max(drawdown)
#
#dailyreturn = Asset1['Strategy'].mean()
##
#dailyvol = Asset1['Strategy'].std()
#sharpe =(dailyreturn/dailyvol)
##
#Portfolio['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#Portfolio['Multiplier'] = Portfolio['Multiplier'].fillna(1)
#drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#MaxDD = max(drawdown)
#print(MaxDD)
##end = t.time()
##totaltime = end - start
##print('Time taken = ', totaltime)
#Portfolio['Multiplier'].plot()
