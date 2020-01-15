# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 01:20:06 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester for the implementation of stop logic
#It probably doesn't work properly, see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

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
start = t.time()
#Input

Ticker1 = 'UVXY'
Ticker2 = '^VIX'

#Remote Signal
Ticker3 = '^VIX'

#Here we go
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)

#Remote Signal
Asset3 = YahooGrabber(Ticker3)

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
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Prepare the remote controller
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
window = 19
a = .42981
b = 1-a
c = 0
d = 0
e = 1.3 #longstop
f = .9 #shortstop
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
Asset3['Price/MA'] = Asset3['Adj Close']/Asset3['MA']
Asset3['Signal'] = np.where(Asset3['Price/MA'] >= 1, 1, 0)
Asset3['CumSignal'] = Asset3['Signal'].cumsum() 
Asset3['CumSignal'].loc[Asset3['CumSignal'] == 0] = 1
Asset3['CumSignalDiff'] = Asset3['CumSignal'].diff()
Asset3['CumSignalDiff'] = Asset3['CumSignalDiff'].fillna(0)
Asset3['Erase'] = np.where(Asset3['Signal'] == Asset3['Signal'].shift(1),
                                     1, 0)
Asset3['Erase'] = np.where(Asset3['Signal'] == 0,
                                     0, Asset3['Erase'])

Asset3['TriggerSignal'] = Asset3['Signal'] - Asset3['Erase']
Asset3['LongPrice'] = np.where(Asset3['TriggerSignal'] == 1, Asset3['Adj Close'], 0)
Asset3['LongPriceFilled'] = Asset3['LongPrice'] 
Asset3['LongPriceFilled'] = np.where(Asset3['LongPriceFilled'] == 0,
                 Asset3['LongPriceFilled'].shift(1), Asset3['LongPriceFilled'])
Asset3['LongPriceFilled'] = Asset3['LongPriceFilled'].fillna(0)  

for m in range(0,20):
    Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'].cumsum() > 1) & 
    (Asset3['LongPriceFilled'] == 0) & (Asset3['LongPriceFilled'].shift(-1) == 0
                    )] = Asset3['LongPriceFilled'].shift(1) 

Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'] == 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = Asset3['LongPriceFilled'].shift(1)
Asset3['LongPriceFilled'].loc[(Asset3['LongPrice'] != 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = 0
    
Asset3['Regime'] = np.where(Asset3['Signal'].shift(1) == 1, 1, 0)
Asset3['CumRegime'] = Asset3['Regime'].cumsum()
Asset3['CumRegimeDiff'] = Asset3['CumRegime'].diff()
Asset3['Counter'] = range(0,len(Asset3))
Asset3['HighDiff'] = Asset3['High'] / Asset3['LongPriceFilled']
Asset3['LowDiff'] = Asset3['Low'] / Asset3['LongPriceFilled']
Asset3 = Asset3.replace([np.inf, -np.inf], np.nan)
Asset3[['HighDiff', 'LowDiff']] = Asset3[['HighDiff', 'LowDiff']].fillna(1)
Asset3['RegimeHighDiff'] = 1
Asset3['RegimeHighDiff'] = np.where(Asset3['Regime'] == 1, Asset3['HighDiff'], 1)
Asset3['RegimeLowDiff'] = 1
Asset3['RegimeLowDiff'] = np.where(Asset3['Regime'] == 1, Asset3['LowDiff'], 1)
Asset3['StopOut'] = 0
Asset3['StopOut'] = np.where(Asset3['RegimeLowDiff'] < f, (f - 1), 0 )
Asset3['StopOut'] = np.where(Asset3['StopOut'].shift(1) == Asset3['StopOut'],
                     0, Asset3['StopOut'])
Asset3['GainOut'] = 0
Asset3['GainOut'] = np.where(Asset3['RegimeHighDiff'] > e, (e-1), 0 )
Asset3['GainOut'] = np.where(Asset3['GainOut'].shift(1) == Asset3['GainOut'],
                     0, Asset3['GainOut'])

Regime = Asset3[['Counter','StopOut','GainOut','CumSignalDiff',
                     'CumRegimeDiff']].loc[(Asset3['RegimeLowDiff'] != 1)]
Regime['NewCounter'] = range(0, len(Regime))

ToDelete = Regime.loc[(Regime['StopOut'] < 0)]
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
for y in NewDelete.Counter:
    Asset3['StopOut'].loc[Asset3['Counter'] == y] = 0
    
Asset3['GainOut'].loc[(Asset3['StopOut'] < 0) & (Asset3['GainOut'] < 0)] = 0

ToDelete = Regime.loc[(Regime['GainOut'] > 0)]
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
for y in NewDelete.Counter:
    Asset3['GainOut'].loc[Asset3['Counter'] == y] = 0
Asset3['Stops'] = Asset3['StopOut'] + Asset3['GainOut']
Asset1['Position'] = a
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                c,a)                                    
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = b
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                d,b)
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)

Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] + 
                            (Asset3['Stops'] * d))

Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
MaxDD = max(drawdown)

dailyreturn = Portfolio['LongShort'].mean()

dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)

Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
MaxDD = max(drawdown)
print(MaxDD)
end = t.time()
totaltime = end - start
print('Time taken = ', totaltime)
Portfolio['Multiplier'].plot()
