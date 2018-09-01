# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 12:52:40 2018

@author: AmatVictoriaCuramIII
"""

#Basic Stop / SMA model

#Lock n' Load
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from pandas import read_csv
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0


#Input

Ticker1 = 'UVXY'

#Here we go
#30MinUVXY
Asset1 = pd.read_csv('UVXYnew.csv')
#Asset1 = Asset1.set_index(Asset1['Date'])
Asset1 = Asset1.reindex(index=Asset1.index[::-1])

#Daily UVXY
#Asset1 = YahooGrabber(Ticker1)

#For CC futures csv
#Asset2 = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\VX1CC.csv', sep = ',')
#Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
#Asset2 = Asset2.set_index('Date')
#Asset2 = Asset2.reindex(index=Asset2.index[::-1])


#Out of Sample Selection
Asset1 = Asset1[:]

##Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#MovingAverage
window = 20
ProfitTarget = .1
#Use positive number
StopLoss = .05
#Define Moving Average
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
Asset1['MA'] = Asset1['MA'].fillna(0)  


#OG regime
#If price is greater than MA then go long. If price < MA go short.
Asset1['Regime'] = np.where(Asset1['MA'] < Asset1['Adj Close'], 1 , -1)                                 

#Wait for MA window to establish regime
#Asset1['Regime'].loc[Asset1['MA'] == 0] = 0
Asset1['OriginalSignal'] = 0
Asset1['OriginalSignal'].loc[Asset1['Regime'] != Asset1['Regime'].shift(1)] = Asset1['Regime']
Asset1['ExposureOnDay'] = Asset1['Regime'].shift(1)
Asset1['ExposureOnDay'] = Asset1['ExposureOnDay'] .fillna(0)
#Trade fill, add slippage here
Asset1['EntryPrice'] = 0
Asset1['EntryPrice'].loc[Asset1['OriginalSignal'] != 0] = Asset1['Adj Close']
Asset1['EntryPriceShifted'] = Asset1['EntryPrice'].shift(1)

#Fill zeros following trade with fill price
for i in range(0,75):
    Asset1['EntryPriceShifted'].loc[(Asset1['EntryPriceShifted'] == 0)] = Asset1['EntryPriceShifted'].shift(1)
Asset1['EntryPriceShifted'] = Asset1['EntryPriceShifted'].fillna(0)

#Based on direction
Asset1['ProfitTarget'] = 0
Asset1['StopLoss'] = 0

#LongProfitTarget
Asset1['ProfitTarget'] = np.where(Asset1['ExposureOnDay'] == 1, Asset1['EntryPriceShifted'] * (1 + ProfitTarget), Asset1['ProfitTarget'])
#LongStopLoss
Asset1['StopLoss'] = np.where(Asset1['ExposureOnDay'] == 1, Asset1['EntryPriceShifted'] * (1 - StopLoss), Asset1['StopLoss'])

#ShortProfitTarget
Asset1['ProfitTarget'] = np.where(Asset1['ExposureOnDay'] == -1, Asset1['EntryPriceShifted'] * (1 - ProfitTarget), Asset1['ProfitTarget'])
#ShortStopLoss
Asset1['StopLoss'] = np.where(Asset1['ExposureOnDay'] == -1, Asset1['EntryPriceShifted'] * (1 + StopLoss), Asset1['StopLoss'])

#Fill zeros  for ProfitTarget and StopLoss
for i in range(0,75):
    Asset1['ProfitTarget'].loc[Asset1['OriginalSignal'] == 0] = Asset1['ProfitTarget']
Asset1['ProfitTarget'] = Asset1['ProfitTarget'].fillna(0)

for i in range(0,75):
    Asset1['StopLoss'].loc[Asset1['OriginalSignal'] == 0] = Asset1['StopLoss']
Asset1['StopLoss'] = Asset1['StopLoss'].fillna(0)

#Directional MaxFavExcursion MaxAdverseExcursion - Entry vs next period High/Low
Asset1['MFE'] = 0
Asset1['MAE'] = 0

#Percentage change from entry price LONG
#Values greater than 1 are gains
Asset1['MFE'] = np.where(Asset1['ExposureOnDay'] == 1, Asset1['High']/Asset1['EntryPriceShifted'], Asset1['MFE'])
#Values less than 1 on MAE are losses
Asset1['MAE'] = np.where(Asset1['ExposureOnDay'] == 1, Asset1['Low']/Asset1['EntryPriceShifted'], Asset1['MAE'])

#Percentage change from entry price SHORT
#Values above 1 are gains
Asset1['MFE'] = np.where(Asset1['ExposureOnDay'] == -1, Asset1['EntryPriceShifted']/Asset1['Low'], Asset1['MFE'])
#Values less than 1 are losses
Asset1['MAE'] = np.where(Asset1['ExposureOnDay'] == -1, Asset1['EntryPriceShifted']/Asset1['High'], Asset1['MAE'])

Asset1['MFE'] = Asset1['MFE'].fillna(0)
Asset1['MAE'] = Asset1['MAE'].fillna(0)

Asset1['TargetHit'] = np.where(Asset1['MFE'] > (1 + ProfitTarget), ProfitTarget, 0)
Asset1['StopHit'] = np.where(Asset1['MAE'] < (1 - StopLoss), -StopLoss, 0)

Asset1['TargetHit'] = np.where(Asset1['ExposureOnDay'] == 0, 0, Asset1['TargetHit'])
Asset1['StopHit'] = np.where(Asset1['ExposureOnDay'] == 0, 0, Asset1['StopHit'])
Asset1['ExposureChange'] = 0
Asset1['ExposureChange'].loc[Asset1['ExposureOnDay'] != Asset1['ExposureOnDay'].shift(1)] = 1
Asset1['ExposureChange'][0] = 0 
Asset1['InTheGame'] = Asset1['ExposureChange']

    
#Pass returns for brackets
Asset1['Brackets'] = 0
#Win on first day
Asset1['Brackets'].loc[(Asset1['ExposureChange'] == 1) & 
    (Asset1['TargetHit'] == ProfitTarget) & (Asset1['StopHit'] == 0)] = ProfitTarget
#Loss on first day
Asset1['Brackets'].loc[(Asset1['ExposureChange'] == 1) &
    (Asset1['StopHit'] == -StopLoss)] = -StopLoss
#redundantcode
Asset1['InTheGame'].loc[(Asset1['ExposureChange'].shift(1) == 1)
    & (Asset1['TargetHit'].shift(1) == 0) & (Asset1['StopHit'].shift(1) == 0)] = 1
    
#this can be considered a time stop 
for x in range(0,20):
#Loop from here
    Asset1['InTheGame'].loc[(Asset1['InTheGame'].shift(1) == 1)
        & (Asset1['TargetHit'].shift(1) == 0) & (Asset1['StopHit'].shift(1) == 0)] = 1
    #Win
    Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureChange'] == 0) 
        & (Asset1['TargetHit'] == ProfitTarget) & (Asset1['StopHit'] == 0)] = ProfitTarget
    #Loss
    Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureChange'] == 0)
        & (Asset1['StopHit'] == -StopLoss)] = -StopLoss
#To here
     
     
Asset1['OpenToEntry'] = Asset1['Open'] / Asset1['EntryPriceShifted']
Asset1['CloseToEntry'] = Asset1['Adj Close'] / Asset1['EntryPriceShifted']

#The case for no bracket hits, long, time exit, on close
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['InTheGame'].shift(-1) == 0)
                        & (Asset1['ExposureOnDay'] == 1)] = (Asset1['CloseToEntry'] - 1)
                        
#The case for no bracket hits, short, time exit, on close
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['InTheGame'].shift(-1) == 0)
                        & (Asset1['ExposureOnDay'] == -1)] = 1 - Asset1['CloseToEntry']

#The case for no bracket hits and position change, long to short
Asset1['Brackets'].loc[(Asset1['ExposureChange'] == 1) & (Asset1['ExposureOnDay'] == 1)
                        & (Asset1['Regime'] == -1)] =  -(1 - Asset1['CloseToEntry'])

#The case for no bracket hits and position change, short to long
Asset1['Brackets'].loc[(Asset1['ExposureChange'] == 1) & (Asset1['ExposureOnDay'] == -1)
                        & (Asset1['Regime'] == 1)] = -(Asset1['CloseToEntry'] - 1)

#The case for gap win days
#If we are long and take gains on open
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureOnDay'] == 1)
                        & (Asset1['OpenToEntry'] >= 1 + ProfitTarget)] = Asset1['OpenToEntry'] - 1
#If we are short and take gains on open     
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureOnDay'] == -1)
                        & (Asset1['OpenToEntry'] <= 1 - ProfitTarget)] = 1 - (Asset1['OpenToEntry'])

#The case for gap loss days
#If we are long and get stopped out short
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureOnDay'] == 1)
                        & (Asset1['OpenToEntry'] <= 1 - StopLoss)] = -(1 - (Asset1['OpenToEntry']))
#If we are short and get stopped out long     
Asset1['Brackets'].loc[(Asset1['InTheGame'] == 1) & (Asset1['ExposureOnDay'] == -1)
                        & (Asset1['OpenToEntry'] >= 1 + StopLoss)] = 1 - (Asset1['OpenToEntry'])
                        
                        
Asset1['Strategy'] = Asset1['Brackets']
#Pass the returns for basic strategy with no brackets
#Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'].shift(1))
#Asset1['Strategy'] = Asset1['Strategy'].fillna(0)
#
#Stats
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
Asset1['Multiplier'] = Asset1['Multiplier'].fillna(1)

drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
MaxDD = max(drawdown)

dailyreturn = Asset1['Strategy'].mean()

dailyvol = Asset1['Strategy'].std()

sharpe =(dailyreturn/dailyvol)

Asset1['Strategy'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))