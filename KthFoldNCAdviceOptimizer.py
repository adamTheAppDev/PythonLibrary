# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 00:50:45 2017

@author: AmatVictoriaCuramIII
"""

#This is the last part of a kth fold optimization tool

import numpy as np
import pandas as pd
import random as rand
#from pandas_datareader import data
#Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
#Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#ticker = '^GSPC'
#s = data.DataReader(ticker, 'yahoo', start='07/01/2007', end='01/01/2050') 
s = pd.read_pickle('SP500NCAdviceJuly07_50') # this is just for testing with a graph
iterations = range(250000)
counter = 0
empty = []
dataset = pd.DataFrame()
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefNCAdviceGiver(Aggregate, q)
#    triumph.append(result)
#    print(r)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice
for i in iterations:
    a = (1 - (rand.random()/2))
    b = (1 - (rand.random()/2))
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    s['Regime'] = np.where(s['Advice'] > a, 1, 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    if s['Strategy'].std() == 0:
        continue
    sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    empty.append(a)
    empty.append(b)
    empty.append(sharpe)
    emptyseries = pd.Series(empty)
    dataset[i] = emptyseries.values
    empty[:] = []
    counter = counter + 1
    print(counter)
#for g in s['LogRet']:
#    slate = endreturns * (1+-g)
#    endreturns = slate
#for h in s['Strategy']:
#    otherslate = endgains * (1+h)
#    endgains = otherslate
#For increased accuracy, remove first window values from TheAdvice
#s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
#                                             figsize = (8,5))
z = dataset.iloc[2]
y = max(z)
x = dataset.columns[(dataset == y).iloc[2]] #this is the column number
print(dataset[x]) #this is the dataframe index based on column number
#print(endreturns)
#print(endgains)
