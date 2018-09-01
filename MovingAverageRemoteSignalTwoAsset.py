# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:03:47 2018

@author: AmatVictoriaCuramIII
"""

#Systematic Volatility Model

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Input

Ticker1 = 'UVXY'
Ticker2 = '^VIX'

#Here we go
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)

#Remote Signal
Asset3 = Asset2

#Asset1 = Asset1.fillna(0)
#Asset2 = Asset2.fillna(0)
#Asset3 = Asset3.fillna(0)


#Match lengths

#Trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]


Asset3 = Asset3[-len(Asset2):]

#Asset2 = Asset2[-600:]

#Log Returns

Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna$INDU(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Prepare the remote controller
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

a = .4244
b = .5755

window = 19
window2 = 31
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()   
Asset3['MA'] = Asset3['MA'].fillna(0)
Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
Asset3['MA2'] = Asset3['MA2'].fillna(0)
Asset1['Position'] = a
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    0, a)
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = b
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    0, b)
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
print(max(drawdown2))

Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] < Asset3['MA2'], 1, 0)

Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])

Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
#Asset3['SignalReturns'].cumsum().apply(np.exp).plot()

SuperFactor = .31
Asset3['Super'] = (Asset3['SignalReturns']*SuperFactor) + Portfolio['LongShort']
Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
SuperMaxDD = max(SuperDrawdown)
superdailyreturn = Asset3['Super'].mean()
superdailyvol = Asset3['Super'].std()
supersharpe =(superdailyreturn/superdailyvol)
print(SuperMaxDD)
Asset3['SuperMultiplier'][:].plot()