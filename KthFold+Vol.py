# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool

#Import modules
#from DefRSIPredictor import DefRSIPredictor
import numpy as np
import pandas as pd
import time as t
import random as rand
#Number of iterations
iterations = range(0,200000)
#Read in data
s = pd.read_pickle('VXXAdvice07_50')
s = s.drop('Regime',1)
s = s.drop('Strategy',1)
#Get short only returns
s['ShortReturns'] = s['LogRet'] * -1
#Empty structures
empty = []
dataset = pd.DataFrame()
#Start timer
start = t.time()
#For number of iterations
for i in iterations:
    #Generate random params
    a = 1 -(rand.random() * 3)
    b = 1 - (rand.random() * 3)
    #Directional methodology
    s['Regime'] = np.where(s['Advice'] > a, 1 , 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    #Apply methodology to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Compounding strategy vs log returns - use np.exp // np.cumsum
    endgains = 1
    endreturns = 1
    for g in s['LogRet']:
        slate = endreturns * (1+g)
        endreturns = slate
    for q in s['Strategy']:
        otherslate = endgains * (1+q)
        endgains = otherslate
    #Constraints
    if endreturns > endgains:
        continue
    if s['Strategy'].std() == 0:
        continue
    #Performance metric
    sharpe = (s['Strategy'].mean()-s['ShortReturns'].mean())/s['Strategy'].std()
    #Constraints
    if sharpe < .007:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(endreturns)
    empty.append(endgains)
    empty.append(sharpe)
    #List to series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[i] = emptyseries.values
    #Clear list
    empty[:] = []
    #Iteration tracking
    print(i)
#End timer    
end = t.time()
#Timer stats
print('Optimization took',end-start,'seconds')
#Metric to sort
z = dataset.iloc[4]
#Top metric
y = max(z)
#Column number
x = dataset.columns[(dataset == y).iloc[4]] 
#Top param set
print(dataset[x])
