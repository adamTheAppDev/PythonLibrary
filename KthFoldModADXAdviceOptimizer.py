# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool

#Import modules
import numpy as np
import pandas as pd
import time as t
import random as rand
#Number of iterations
iterations = range(0,1900000)
#Read in data
s = pd.read_pickle('RUTModADXAGGAdviceColumn94_07')
s = s.drop('Regime',1)
s = s.drop('Strategy',1)
#Assign data structures
empty = []
dataset = pd.DataFrame()
start = t.time()
#For number of iterations
for i in iterations:
    #Generate random variables
    a = 1 - (rand.random() * 3)
    b = 1 - (rand.random() * 3)
    #Directional methodology
    s['Regime'] = np.where(s['Advice'] > a, 1 , 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Ones
    endgains = 1
    endreturns = 1
    #Constraints
    if s['Strategy'].std() == 0:
        continue
    #Performance metrics
    s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    #Constraints
    if s['sharpe'][-1] < -.01:
        continue
    #Bad metrics to use
    s['CorrectNextDay'] =  np.where(s['Regime'] == 1, s['High'].shift(
                                            -1) > s['Adj Close'] , 0)
    s['CorrectNextDay'] =  np.where(s['Regime'] == -1, s['Low'].shift(
                             -1) < s['Adj Close'] , s['CorrectNextDay'])
    s['ModCND'] = np.where(s['Regime'] == 0, 1, 0)
    s['ModCND'] = s['ModCND'] + s['CorrectNextDay']
    #Bad metric
    winrate = sum(s['ModCND']/len(s))
    #Add params to list
    empty.append(a)
    empty.append(b)
#    empty.append(endreturns)
#    empty.append(endgains)
    empty.append(s['sharpe'][-1])
    empty.append(winrate)
    #List to Series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[i] = emptyseries.values
    #Clear list
    empty[:] = []
#    print(i)
#End timer
end = t.time()
#Timer stats
print('Optimization took',end-start,'seconds')
#All of metric
z = dataset.iloc[2]
#Top metric
y = max(z)
#Top param set
x = dataset.columns[(dataset == y).iloc[2]] #this is the column number
#Display results
print(dataset[x]) #this is the dataframe index based on column number
#Timer stats
print(end - start,'seconds')
