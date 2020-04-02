# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a short only, martingale style, volatility trading strategy 
#that takes incrementally larger positions

#Import modules 
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Assign tickers
Ticker1 = '^VIX'
Ticker2 = 'UVXY'
#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset1 = Asset1[-len(Asset2):] #In

#Range index 
Asset1['SubIndex'] = range(1,len(Asset1)+1)

#Variable windows
MinWindow = 52
HoldPeriod = 80
ATRWindow = 20
Counter = 0
PositionSize = 3 #PERCENT!
UniformMove = .07
PositionScale = .2#PERCENT!

#Calculate log Returns
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Calculate ATR
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)
Asset1['ATR'] = Asset1['TrueRange'].rolling(window = ATRWindow,
                                center=False).mean()

#Market top and bottom calculation
#Asset1['RollingMax'] = Asset1['High'].rolling(window=donchianwindow, center=False).max()
Asset1['RollingMin'] = Asset1['Low'].rolling(window=MinWindow, center=False).min()
#High price over rolling minimum
Asset1['HighOverRollingMin'] = Asset1['High']/Asset1['RollingMin']

#Unit 1
Asset1['UnitOne'] = 0
Asset1['UnitOne'] = np.where(Asset1['HighOverRollingMin'] > 1 + (1 * UniformMove), PositionSize, 0)
for i in range(0,HoldPeriod):
    Asset1['UnitOne'] = np.where(Asset1['UnitOne'].shift(1) == PositionSize, PositionSize, Asset1['UnitOne'])
#Unit 2
Asset1['UnitTwo'] = 0
Asset1['UnitTwo'] = np.where(Asset1['HighOverRollingMin'] > 1 + (2 * UniformMove), (PositionSize + (1 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitTwo'] = np.where(Asset1['UnitTwo'].shift(1) == (PositionSize + (1 * PositionScale)), (PositionSize + (1 * PositionScale)), Asset1['UnitTwo'])
#Unit 3
Asset1['UnitThree'] = 0
Asset1['UnitThree'] = np.where(Asset1['HighOverRollingMin'] > 1 + (3 * UniformMove), (PositionSize + (2 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitThree'] = np.where(Asset1['UnitThree'].shift(1) == (PositionSize + (2 * PositionScale)), (PositionSize + (2 * PositionScale)), Asset1['UnitThree'])
#Unit 4
Asset1['UnitFour'] = 0
Asset1['UnitFour'] = np.where(Asset1['HighOverRollingMin'] > 1 + (4 * UniformMove), (PositionSize + (3 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitFour'] = np.where(Asset1['UnitFour'].shift(1) == (PositionSize + (3 * PositionScale)), (PositionSize + (3 * PositionScale)), Asset1['UnitFour'])
#Unit 5
Asset1['UnitFive'] = 0
Asset1['UnitFive'] = np.where(Asset1['HighOverRollingMin'] > 1 + (5 * UniformMove), (PositionSize + (4 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitFive'] = np.where(Asset1['UnitFive'].shift(1) == (PositionSize + (4 * PositionScale)), (PositionSize + (4 * PositionScale)), Asset1['UnitFive'])
#Unit 6
Asset1['UnitSix'] = 0
Asset1['UnitSix'] = np.where(Asset1['HighOverRollingMin'] > 1 + (6 * UniformMove), (PositionSize + (5 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitSix'] = np.where(Asset1['UnitSix'].shift(1) == (PositionSize + (5 * PositionScale)), (PositionSize + (5 * PositionScale)), Asset1['UnitSix'])
#Unit 7
Asset1['UnitSeven'] = 0
Asset1['UnitSeven'] = np.where(Asset1['HighOverRollingMin'] > 1 + (7 * UniformMove), (PositionSize + (6 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitSeven'] = np.where(Asset1['UnitSeven'].shift(1) == (PositionSize + (6 * PositionScale)), (PositionSize + (6 * PositionScale)), Asset1['UnitSeven'])
#Unit 8
Asset1['UnitEight'] = 0
Asset1['UnitEight'] = np.where(Asset1['HighOverRollingMin'] > 1 + (8 * UniformMove), (PositionSize + (7 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitEight'] = np.where(Asset1['UnitEight'].shift(1) == (PositionSize + (7 * PositionScale)), (PositionSize + (7 * PositionScale)), Asset1['UnitEight'])
#Unit 9
Asset1['UnitNine'] = 0
Asset1['UnitNine'] = np.where(Asset1['HighOverRollingMin'] > 1 + (9 * UniformMove), (PositionSize + (8 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitNine'] = np.where(Asset1['UnitNine'].shift(1) == (PositionSize + (8 * PositionScale)), (PositionSize + (8 * PositionScale)), Asset1['UnitNine'])
#Unit 10
Asset1['UnitTen'] = 0
Asset1['UnitTen'] = np.where(Asset1['HighOverRollingMin'] > 1 + (10 * UniformMove), (PositionSize + (9 * PositionScale)), 0)
for i in range(0,HoldPeriod):
    Asset1['UnitTen'] = np.where(Asset1['UnitTen'].shift(1) == (PositionSize + (9 * PositionScale)), (PositionSize + (9 * PositionScale)), Asset1['UnitTen'])
#Unit 11
Asset1['UnitEleven'] = 0
Asset1['UnitEleven'] = np.where(Asset1['HighOverRollingMin'] > 1 + (11 * UniformMove), PositionSize, 0)
for i in range(0,HoldPeriod):
    Asset1['UnitEleven'] = np.where(Asset1['UnitEleven'].shift(1) == PositionSize, PositionSize, Asset1['UnitEleven'])

#Adding position sizes
Asset1['SumUnits'] = Asset1[['UnitOne','UnitTwo','UnitThree','UnitFour',
    'UnitFive','UnitSix','UnitSeven','UnitEight','UnitNine','UnitTen','UnitEleven']].sum(axis = 1)
#Exposure methodology
Asset1['Regime'] = np.where(Asset1['SumUnits'] >= 1, -1,0)
Asset2['Strategy'] = Asset1['Regime'].shift(1) * Asset2['LogRet'] * (Asset1['SumUnits']/100)
Asset2['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
#Returns on $1
Asset2['Multiplier'] = Asset2['Strategy'].cumsum().apply(np.exp)

#Incorrectly calculated drawdown statistic
drawdown =  1 - Asset2['Multiplier'].div(Asset2['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)
#Performance metrics
dailyreturn = Asset2['Strategy'].mean()
dailyvol = Asset2['Strategy'].std()
