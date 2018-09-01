# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 19:13:12 2018

@author: AmatVictoriaCuramIII
"""

#Drag w/ Increment
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Inputs - OHLC data
Ticker1 = 'UVXY'
Asset1 = YahooGrabber(Ticker1)
Asset1 = Asset1[:] #In
#
#Numbered subindex 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Variable windows
ROCWindow = 31
HoldPeriod = 68
ATRWindow = 20
Counter = 0
PositionSize = 1.4#PERCENT!
UniformMove = .08
PositionScale = .6#PERCENT!
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
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRWindow,
                                center=False).mean()
Asset1['RateOfChange'] = (Asset1['Adj Close'] - Asset1['Adj Close'].shift(ROCWindow)
                                      ) / Asset1['Adj Close'].shift(ROCWindow)
Bottom = Asset1['RateOfChange'].min()
#Unit 1
Asset1['UnitOne'] = 0
Asset1['UnitOne'] = np.where(Asset1['RateOfChange'] > Bottom + (1 * UniformMove), PositionSize, 0)
for i in range(0,HoldPeriod):
    Asset1['UnitOne'] = np.where(Asset1['UnitOne'].shift(1) == PositionSize, PositionSize, Asset1['UnitOne'])
#Unit 2
Asset1['UnitTwo'] = 0
Asset1['UnitTwo'] = np.where(Asset1['RateOfChange'] > Bottom + (2 * UniformMove), (PositionSize + (1 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitTwo'] = np.where(Asset1['UnitTwo'].shift(1) == (PositionSize + (1 * PositionScale)), (PositionSize + (1 * PositionScale)), Asset1['UnitTwo'])
#Unit 3
Asset1['UnitThree'] = 0
Asset1['UnitThree'] = np.where(Asset1['RateOfChange'] > Bottom + (3 * UniformMove), (PositionSize + (2 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitThree'] = np.where(Asset1['UnitThree'].shift(1) == (PositionSize + (2 * PositionScale)), (PositionSize + (2 * PositionScale)), Asset1['UnitThree'])
#Unit 4
Asset1['UnitFour'] = 0
Asset1['UnitFour'] = np.where(Asset1['RateOfChange'] > Bottom + (4 * UniformMove), (PositionSize + (3 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitFour'] = np.where(Asset1['UnitFour'].shift(1) == (PositionSize + (3 * PositionScale)), (PositionSize + (3 * PositionScale)), Asset1['UnitFour'])
#Unit 5
Asset1['UnitFive'] = 0
Asset1['UnitFive'] = np.where(Asset1['RateOfChange'] > Bottom + (5 * UniformMove), (PositionSize + (4 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitFive'] = np.where(Asset1['UnitFive'].shift(1) == (PositionSize + (4 * PositionScale)), (PositionSize + (4 * PositionScale)), Asset1['UnitFive'])
#Unit 6
Asset1['UnitSix'] = 0
Asset1['UnitSix'] = np.where(Asset1['RateOfChange'] > Bottom + (6 * UniformMove), (PositionSize + (5 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitSix'] = np.where(Asset1['UnitSix'].shift(1) == (PositionSize + (5 * PositionScale)), (PositionSize + (5 * PositionScale)), Asset1['UnitSix'])
#Unit 7
Asset1['UnitSeven'] = 0
Asset1['UnitSeven'] = np.where(Asset1['RateOfChange'] > Bottom + (7 * UniformMove), (PositionSize + (6 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitSeven'] = np.where(Asset1['UnitSeven'].shift(1) == (PositionSize + (6 * PositionScale)), (PositionSize + (6 * PositionScale)), Asset1['UnitSeven'])
#Unit 8
Asset1['UnitEight'] = 0
Asset1['UnitEight'] = np.where(Asset1['RateOfChange'] > Bottom + (8 * UniformMove), (PositionSize + (7 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitEight'] = np.where(Asset1['UnitEight'].shift(1) == (PositionSize + (7 * PositionScale)), (PositionSize + (7 * PositionScale)), Asset1['UnitEight'])
#Unit 9
Asset1['UnitNine'] = 0
Asset1['UnitNine'] = np.where(Asset1['RateOfChange'] > Bottom + (9 * UniformMove), (PositionSize + (8 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitNine'] = np.where(Asset1['UnitNine'].shift(1) == (PositionSize + (8 * PositionScale)), (PositionSize + (8 * PositionScale)), Asset1['UnitNine'])
#Unit 10
Asset1['UnitTen'] = 0
Asset1['UnitTen'] = np.where(Asset1['RateOfChange'] > Bottom + (10 * UniformMove), (PositionSize + (9 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitTen'] = np.where(Asset1['UnitTen'].shift(1) == (PositionSize + (9 * PositionScale)), (PositionSize + (9 * PositionScale)), Asset1['UnitTen'])
#Unit 11
Asset1['UnitEleven'] = 0
Asset1['UnitEleven'] = np.where(Asset1['RateOfChange'] > Bottom + (11 * UniformMove), PositionSize, 0)
for i in range(0,HoldPeriod):
    Asset1['UnitEleven'] = np.where(Asset1['UnitEleven'].shift(1) == PositionSize, PositionSize, Asset1['UnitEleven'])


Asset1['SumUnits'] = Asset1[['UnitOne','UnitTwo','UnitThree','UnitFour',
    'UnitFive','UnitSix','UnitSeven','UnitEight','UnitNine','UnitTen','UnitEleven']].sum(axis = 1)

Asset1['Regime'] = np.where(Asset1['SumUnits'] >= 1, -1,0)
Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet'] * (Asset1['SumUnits']/100)
Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()