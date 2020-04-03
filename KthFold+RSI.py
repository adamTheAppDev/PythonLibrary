# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a tester for part a kth fold optimization.

#Import modules
#from DefRSIPredictor import DefRSIPredictor
import numpy as np
import pandas as pd
import time as t
import random as rand
#Number of iterations
iterations = range(0,10000)
#Read in data
s = pd.read_pickle('RUTAGGAdvice07_50')
s = s.drop('Regime',1)
s = s.drop('Strategy',1)
#Empty data structures
empty = []
dataset = pd.DataFrame()
#Start timer
start = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = 1 - (rand.random() * 3)
    b = 1 - (rand.random() * 3)
    #Directional methodology
    s['Regime'] = np.where(s['Advice'] > a, 1 , 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    #Apply to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Strategy vs log return compounding - use np.exp
    endgains = 1
    endreturns = 1
    for g in s['LogRet']:
        slate = endreturns * (1+g)
        endreturns = slate
    for q in s['Strategy']:
        otherslate = endgains * (1+q)
        endgains = otherslate
    if endreturns > endgains:
        continue
    #Constraints
    if s['Strategy'].std() == 0:
        continue
    #Metrics    
    sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    #Constraints
    if sharpe < .005:
        continue
    #Bad statistic
    s['CorrectNextDay'] =  np.where(s['Regime'] == 1, s['High'].shift(
                                            -1) > s['Adj Close'] , 0)
    s['CorrectNextDay'] =  np.where(s['Regime'] == -1, s['Low'].shift(
                             -1) < s['Adj Close'] , s['CorrectNextDay'])
    winrate = sum(s['CorrectNextDay'])/len(s)
    #Add params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(endreturns)
    empty.append(endgains)
    empty.append(sharpe)
    empty.append(winrate)
    #List to series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[i] = emptyseries.values
    #Clelar list
    empty[:] = []
    #Iteration tracking
    print(i)
#End timer    
end = t.time()
#Timer stats
print('Optimization took',end-start,'seconds')
#Metric to sort
z = dataset.iloc[5]
#Top metric
y = max(z)
#Column ID
x = dataset.columns[(dataset == y).iloc[5]] 
#Top param set
print(dataset[x])
