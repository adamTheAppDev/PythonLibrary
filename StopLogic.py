# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester for the implementation of stop logic
#There is faulty logic, see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py

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
Counter = 0

#Start timer
start = t.time()

#Input tickers
Ticker1 = 'UVXY'
Ticker2 = '^VIX'
Ticker3 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = YahooGrabber(Ticker3)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Match lengths
Asset3 = Asset3[-len(Asset2):]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Variable assignment
window = 19
a = .42981
b = 1-a
c = 0
d = 0
e = 1.3 #long stop
f = .9 #short stop

#Calculate simple moving average
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
#Price to moving average
Asset3['Price/MA'] = Asset3['Adj Close']/Asset3['MA']
#Directional methodology
Asset3['Signal'] = np.where(Asset3['Price/MA'] >= 1, 1, 0)
#Sum of signals
Asset3['CumSignal'] = Asset3['Signal'].cumsum() 
Asset3['CumSignal'].loc[Asset3['CumSignal'] == 0] = 1
Asset3['CumSignalDiff'] = Asset3['CumSignal'].diff()
Asset3['CumSignalDiff'] = Asset3['CumSignalDiff'].fillna(0)

#If signal in previous period, erase signal in period
Asset3['Erase'] = np.where(Asset3['Signal'] == Asset3['Signal'].shift(1),
                                     1, 0)
Asset3['Erase'] = np.where(Asset3['Signal'] == 0,
                                     0, Asset3['Erase'])

#Remove additional signals
Asset3['TriggerSignal'] = Asset3['Signal'] - Asset3['Erase']

#Calculate fill price
Asset3['LongPrice'] = np.where(Asset3['TriggerSignal'] == 1, Asset3['Adj Close'], 0)
Asset3['LongPriceFilled'] = Asset3['LongPrice'] 
Asset3['LongPriceFilled'] = np.where(Asset3['LongPriceFilled'] == 0,
                 Asset3['LongPriceFilled'].shift(1), Asset3['LongPriceFilled'])
Asset3['LongPriceFilled'] = Asset3['LongPriceFilled'].fillna(0)  

#Forward fill for holding period
for m in range(0,20):
    Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'].cumsum() > 1) & 
    (Asset3['LongPriceFilled'] == 0) & (Asset3['LongPriceFilled'].shift(-1) == 0
                    )] = Asset3['LongPriceFilled'].shift(1) 

#Calculate fill price
Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'] == 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = Asset3['LongPriceFilled'].shift(1)
Asset3['LongPriceFilled'].loc[(Asset3['LongPrice'] != 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = 0

#Directional methodology
Asset3['Regime'] = np.where(Asset3['Signal'].shift(1) == 1, 1, 0)
#Sum of regime
Asset3['CumRegime'] = Asset3['Regime'].cumsum()
Asset3['CumRegimeDiff'] = Asset3['CumRegime'].diff()
#Iterable
Asset3['Counter'] = range(0,len(Asset3))
#Percent difference between high price and fill price
Asset3['HighDiff'] = Asset3['High'] / Asset3['LongPriceFilled']
Asset3['LowDiff'] = Asset3['Low'] / Asset3['LongPriceFilled']
#Sub infinite values
Asset3 = Asset3.replace([np.inf, -np.inf], np.nan)
#Fill nans 
Asset3[['HighDiff', 'LowDiff']] = Asset3[['HighDiff', 'LowDiff']].fillna(1)
#Ones
Asset3['RegimeHighDiff'] = 1
Asset3['RegimeHighDiff'] = np.where(Asset3['Regime'] == 1, Asset3['HighDiff'], 1)
#Ones
Asset3['RegimeLowDiff'] = 1
Asset3['RegimeLowDiff'] = np.where(Asset3['Regime'] == 1, Asset3['LowDiff'], 1)
#Zeroes
Asset3['StopOut'] = 0
Asset3['StopOut'] = np.where(Asset3['RegimeLowDiff'] < f, (f - 1), 0 )
#Stop out
Asset3['StopOut'] = np.where(Asset3['StopOut'].shift(1) == Asset3['StopOut'],
                     0, Asset3['StopOut'])
#Zeroes
Asset3['GainOut'] = 0
Asset3['GainOut'] = np.where(Asset3['RegimeHighDiff'] > e, (e-1), 0 )
#Profit taker
Asset3['GainOut'] = np.where(Asset3['GainOut'].shift(1) == Asset3['GainOut'],
                     0, Asset3['GainOut'])
#Create new dataframe
Regime = Asset3[['Counter', 'StopOut', 'GainOut', 'CumSignalDiff',
                     'CumRegimeDiff']].loc[(Asset3['RegimeLowDiff'] != 1)]
#Iterable
Regime['NewCounter'] = range(0, len(Regime))

#Create dataframe
ToDelete = Regime.loc[(Regime['StopOut'] < 0)]
#Difference
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
#Create dataframe
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
#Delete values
for y in NewDelete.Counter:
    Asset3['StopOut'].loc[Asset3['Counter'] == y] = 0
#Clear values    
Asset3['GainOut'].loc[(Asset3['StopOut'] < 0) & (Asset3['GainOut'] < 0)] = 0
#Add column to dataframe
ToDelete = Regime.loc[(Regime['GainOut'] > 0)]
#Difference
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
#Create dataframe
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
#Delete values
for y in NewDelete.Counter:
    Asset3['GainOut'].loc[Asset3['Counter'] == y] = 0
#Positions being exited    
Asset3['Stops'] = Asset3['StopOut'] + Asset3['GainOut']
#Position sizing
Asset1['Position'] = a
#Alternative position sizing
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                c,a)                                    
#Apply positions to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = b
#Alternative position sizing
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                d,b)
#Apply positions to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass individual return streams to dataframe
Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)

#Cumulative portfolio returns 
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] + 
                            (Asset3['Stops'] * d))
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Incorrectly calculated drawdown statistic
drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
MaxDD = max(drawdown)

dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)

#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Display results
print(MaxDD)
#End timer
end = t.time()
#Timer stats
totaltime = end - start
print('Time taken = ', totaltime)
#Graphical display
Portfolio['Multiplier'].plot()
