# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a trading strategy tool

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Empty data structures
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Assign tickers
Ticker1 = 'UVXY'
Ticker2 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = Asset2

#Match lengths
#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

Asset3 = Asset3[-len(Asset2):]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna$INDU(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Position sizing
a = .4244
b = .5755
#Assign params
window = 19
window2 = 31
#Calculate moving average
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()   
Asset3['MA'] = Asset3['MA'].fillna(0)
Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
Asset3['MA2'] = Asset3['MA2'].fillna(0)
#Position sizing
Asset1['Position'] = a
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    0, a)
#Apply positions to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = b
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    0, b)
#Apply positions to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1) #Pass short position to portfolio
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)#Pass long position to portfolio
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
#Cumulative returns
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Incorrectly calculated drawdown statistic
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
print(max(drawdown2))

#Directional methodology
Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] < Asset3['MA2'], 1, 0)
#Volatility regime
Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])
#Regime change
Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
#Asset3['SignalReturns'].cumsum().apply(np.exp).plot()
#Leverage factor
SuperFactor = .31
#New regime returns
Asset3['Super'] = (Asset3['SignalReturns']*SuperFactor) + Portfolio['LongShort']
#Returns on $1
Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
#Incorrectly calculated drawdown statistic
SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
SuperMaxDD = max(SuperDrawdown)
#Performance metrics
superdailyreturn = Asset3['Super'].mean()
superdailyvol = Asset3['Super'].std()
supersharpe =(superdailyreturn/superdailyvol)
#Incorrect
print(SuperMaxDD)
#Graphical display
Asset3['SuperMultiplier'][:].plot()
