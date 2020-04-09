# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is the last part of a kth fold optimization tool

#Import modules
import numpy as np
import pandas as pd
import random as rand
#from pandas_datareader import data

#Read in data
#Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
#Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#s = data.DataReader(ticker, 'yahoo', start='07/01/2007', end='01/01/2050') 
s = pd.read_pickle('SP500NCAdviceJuly07_50') # this is just for testing with a graph
#Assign ticker
#ticker = '^GSPC'
#Variable assignment
iterations = range(250000)
counter = 0
empty = []
dataset = pd.DataFrame()
#Incrementally larger time series
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefNCAdviceGiver(Aggregate, q)
#    triumph.append(result)
#    print(r)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice
#For all iterations
for i in iterations:
    #Generate random params
    a = (1 - (rand.random()/2))
    b = (1 - (rand.random()/2))
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    #Directional methodology
    s['Regime'] = np.where(s['Advice'] > a, 1, 0)
    s['Regime'] = np.where(s['Advice'] < b, -1, s['Regime'])
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Constraints
    if s['Strategy'].std() == 0:
        continue
    #Performance metrics
    sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    #Save params and metrics
    empty.append(a)
    empty.append(b)
    empty.append(sharpe)
    #List to Series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[i] = emptyseries.values
    #Clear list
    empty[:] = []
    #Iteration tracking
    counter = counter + 1
    print(counter)
    
#Compounding returns
#for g in s['LogRet']:
#    slate = endreturns * (1+-g)
#    endreturns = slate
#for h in s['Strategy']:
#    otherslate = endgains * (1+h)
#    endgains = otherslate
#Graphical display 
#For increased accuracy, remove first window values from TheAdvice
#s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
#                                             figsize = (8,5))
#Metric of choice
z = dataset.iloc[2]
#Top metric
y = max(z)
#Top metric column number
x = dataset.columns[(dataset == y).iloc[2]] 
#Top param set
print(dataset[x]) #this is the dataframe index based on column number
