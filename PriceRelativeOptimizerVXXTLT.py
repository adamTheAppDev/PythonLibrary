# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
empty = []
dataset = pd.DataFrame()
asone = pd.DataFrame()
start = t.time()
counter = 0

Asset1 = DatabaseGrabber('UVXY')
Asset2 = DatabaseGrabber('VXX')

trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[-trim:]
    else:
        Asset2 = Asset2[trim:]

Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

iterations = range(0, 1000)
for i in iterations:
    counter = counter + 1
    a = rand.random()
    b = 1 - a
    Asset1['Position'] = b
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = a
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    asone['VXXpass'] = Asset1['Pass']
    asone['TLTpass'] = Asset2['Pass']
    asone['PriceRelative'] = Asset2['Adj Close'] / Asset1['Adj Close']
    #asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
    asone['LongShort'] = (Asset1['Pass']) + (-1 * Asset2['Pass']) 
#    asone = asone[:-2]
#    asone['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    dailyreturn = asone['LongShort'].mean()
    if dailyreturn < .001:
        continue
    dailyvol = asone['LongShort'].std()
    if asone['LongShort'].std() == 0:    
        continue
    sharpe =(dailyreturn/(dailyvol))
    if sharpe < 0.0194:     
        continue
    portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
    maxdd = 0
    tempdd = 0 
    highwater = 1
    ranger = range(0,len(portfoliomultiplier))
    for r in ranger:
        currentvalue = portfoliomultiplier[r]
        if highwater == 0:
            currentvalue = highwater
        if currentvalue > highwater:
            highwater = currentvalue
        else:
            tempdd = 1 - (currentvalue/highwater)
        if tempdd > maxdd:
            maxdd = tempdd
            tempdd = 0
#    print(counter)    
    empty.append(a)
    empty.append(b)
    empty.append(sharpe)
    empty.append(sharpe/maxdd)
    empty.append(dailyreturn/maxdd)
    emptyseries = pd.Series(empty)
    dataset[i] = emptyseries.values
    empty[:] = [] 
z1 = dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = dataset.columns[(dataset == j).iloc[3]]    
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
y = max(z1)
k = dataset.columns[(dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])
end = t.time()
print(end-start, 'seconds later')
print(dataset[k])




TLT['Position'] = (dataset[kfloat][0])
TLT['Pass'] = (TLT['LogRet'] * TLT['Position'])
Asset1['Position'] = (dataset[kfloat][1])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
VIX['Position'] = .5
VIX['Pass'] = VIX['LogRet'] * VIX['Position']
VXV['Position'] = .5
VXV['Pass'] = VXV['LogRet'] * VXV['Position']
TLT['Position'] = .5
TLT['Pass'] = TLT['LogRet'] * TLT['Position']
asone['VXXpass'] = Asset1['Pass']
asone['UVXYpass'] = Asset2['Pass']
asone['PriceRelative'] = Asset1['Adj Close'] / TLT['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
asone['LongShort'] = Asset2['Pass'] + (-1 * Asset1['Pass']) 
asone = asone[:-2]
asone['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = asone['LongShort'].mean()
dailyvol = asone['LongShort'].std()
sharpe =(dailyreturn)
portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
maxdd = 0
tempdd = 0 
highwater = 1
ranger = range(0,len(portfoliomultiplier))
for r in ranger:
    currentvalue = portfoliomultiplier[r]
    if highwater == 0:
        currentvalue = highwater
    if currentvalue > highwater:
        highwater = currentvalue
    else:
        tempdd = 1 - (currentvalue/highwater)
    if tempdd > maxdd:
        maxdd = tempdd
        tempdd = 0
print('Max drawdown is ' + str(maxdd))
conversionfactor = asone['PriceRelative'][-1]
