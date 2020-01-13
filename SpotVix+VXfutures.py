# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuram
"""

#This is strategy tester for spot VIX + VX futures strategy - 2 asset portfolio

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

Ticker1 = '^VIX'

#Here we go
Asset1 = YahooGrabber(Ticker1)
#Asset2 = YahooGrabber(Ticker2)
Asset1 = Asset1[:-1]
#For CC futures csv
Asset2 = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\OVXCLS.csv', sep = ',')
Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
Asset2 = Asset2.set_index('Date')
#Asset2 = Asset2.reindex(index=Asset2.index[::-1])


#Remote Signal
#Asset3 = YahooGrabber(Ticker1)

#Match lengths

##Trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

##Log Returns
#
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
##
##
##Brute Force Optimization
iterations = range(0, 1000)
#for i in iterations:
Counter = Counter + 1
a = 1 #rand.random()
b = -1
c = 0#rand.random()
d = 0#rand.random()
#if c + d > 1:
#    continue
e = 5#rand.randint(3,100)
window = int(e)
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
  #  Asset3['MA'] = Asset3['MA'].fillna(0)
Asset1['STD'] = Asset1['LogRet'].rolling(window=window, center=False).std()
Asset1['STDSTD'] = Asset1['STD'].rolling(window=window, center=False).std()

Asset1['meanSTD'] = Asset1['STD'].rolling(window=window, center=False).mean()
Asset1['meanSTDSTD'] = Asset1['STDSTD'].rolling(window=window, center=False).mean()
Asset1['Trend'] = np.where(Asset1['Adj Close'].shift(1) < Asset1['MA'].shift(1),
                                b,a)                                    
Asset1['Position'] = 0
#Asset1['Trend'].loc[(Asset1[ ])]
Asset1['Signal'] = np.where(Asset1['STDSTD'] > Asset1['meanSTDSTD'], 1, 0)
Asset1['Position'].loc[(Asset1['Signal'] == 1) & (Asset1['Trend'] == 1)] = 1
#Asset1['Position'].loc[(Asset1['Signal'] == 1) & (Asset1['Trend'] == -1)] = -1
Asset1['Pass'] = (Asset2['LogRet'] * Asset1['Position'])


Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
MaxDD = max(drawdown)
#    if MaxDD > float(.21): 
#        continue

dailyreturn = Asset1['Pass'].mean()
#if dailyreturn < .0003:
#    continue

dailyvol = Asset1['Pass'].std()
sharpe =(dailyreturn/dailyvol)

Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
MaxDD = max(drawdown)
print(Counter)
Empty.append(a)
Empty.append(b)
Empty.append(c)
Empty.append(d)
Empty.append(e)
Empty.append(sharpe)
Empty.append(sharpe/MaxDD)
Empty.append(dailyreturn/MaxDD)
Empty.append(MaxDD)
Emptyseries = pd.Series(Empty)
Dataset[0] = Emptyseries.values
#Dataset[i] = Emptyseries.values
Empty[:] = [] 
    
Asset1 = Asset1[window*3:]   
Asset2 = Asset2[window*3:]
Asset1['Multiplier'].plot()    
#z1 = Dataset.iloc[6]
#w1 = np.percentile(z1, 80)
#v1 = [] #this variable stores the Nth percentile of top performers
#DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
#for h in z1:
#    if h > w1:
#      v1.append(h)
#for j in v1:
#      r = Dataset.columns[(Dataset == j).iloc[6]]    
#      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#y = max(z1)
#k = Dataset.columns[(Dataset == y).iloc[6]] #this is the column number
#kfloat = float(k[0])
#End = t.time()
#print(End-Start, 'seconds later')
#print(Dataset[k])
#
#window = int((Dataset[kfloat][4]))
#Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()   
#
##Asset1['Position'] = (Dataset[kfloat][0])
#Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) < Asset1['MA'].shift(1),
#                                    Dataset[kfloat][2],Dataset[kfloat][0])
##Asset1['Position'].loc[(Asset3['MA'] == 0)] = 0
#Asset1['Pass'] = (Asset2['LogRet'] * Asset1['Position'])
##Asset2['Position'] = (Dataset[kfloat][1])
##Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
##                                    Dataset[kfloat][3],Dataset[kfloat][1])
##Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#
##Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
##Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
##Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
##asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
##Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Asset1['Pass'][:].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
#dailyreturn = Asset1['Pass'].mean()
#dailyvol = Asset1['Pass'].std()
#sharpe =(dailyreturn/dailyvol)
#Portfolio['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
#drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
##conversionfactor = Portfolio['PriceRelative'][-1]
#print(max(drawdown2))
##pd.to_pickle(Portfolio, 'VXX:UVXY')
