# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 20:05:59 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
import pandas as pd
import time as t
import random as rand
iterations = range(0,1900000)
s = pd.read_pickle('RUTModADXAGGAdviceColumn94_07')
s = s.drop('Regime',1)
s = s.drop('Strategy',1)
empty = []
dataset = pd.DataFrame()
start = t.time()
for i in iterations:
    a = 1 - (rand.random() * 3)
    b = 1 - (rand.random() * 3)
    s['Regime'] = np.where(s['Advice'] > a, 1 , 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    endgains = 1
    endreturns = 1
#    for g in s['LogRet']:
#        slate = endreturns * (1+g)
#        endreturns = slate
#    for q in s['Strategy']:
#        otherslate = endgains * (1+q)
#        endgains = otherslate
#    if endreturns > endgains:
#        continue
    if s['Strategy'].std() == 0:
        continue
    s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    if s['sharpe'][-1] < -.01:
        continue
    s['CorrectNextDay'] =  np.where(s['Regime'] == 1, s['High'].shift(
                                            -1) > s['Adj Close'] , 0)
    s['CorrectNextDay'] =  np.where(s['Regime'] == -1, s['Low'].shift(
                             -1) < s['Adj Close'] , s['CorrectNextDay'])
    s['ModCND'] = np.where(s['Regime'] == 0, 1, 0)
    s['ModCND'] = s['ModCND'] + s['CorrectNextDay']

    winrate = sum(s['ModCND']/len(s))
    empty.append(a)
    empty.append(b)
#    empty.append(endreturns)
#    empty.append(endgains)
    empty.append(s['sharpe'][-1])
    empty.append(winrate)
    emptyseries = pd.Series(empty)
    dataset[i] = emptyseries.values
    empty[:] = []
#    print(i)
end = t.time()
print('Optimization took',end-start,'seconds')
z = dataset.iloc[2]
y = max(z)
x = dataset.columns[(dataset == y).iloc[2]] #this is the column number
print(dataset[x]) #this is the dataframe index based on column number
print(end - start,'seconds')