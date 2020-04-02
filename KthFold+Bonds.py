# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool

#Import modules
from DefRSIPredictor import DefRSIPredictor
import numpy as np
import pandas as pd
from YahooGrabber import YahooGrabber

#Read in data
Aggregate = pd.read_pickle('TLTAGGSHARPE023')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Assign ticker
ticker = 'TMF'
#Request/read in data
s = YahooGrabber(ticker)
s1 = pd.read_pickle('TLTAGGAdvice07_50') # this is just for testing with a graph
#Transfer column
s['Advice'] = s1['Advice']
#Iterable
#ranger = range(1,len(s)+1)
#Creating recurrent incremental data ranges
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefRSIPredictor(Aggregate, q)
#    triumph.append(result)
#    print(r)
#    print(result)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Directional methodology
s['Regime'] = np.where(s['Advice'] > .706102, 1, 0)
s['Regime'] = np.where(s['Advice'] < -.644197, -1, s['Regime'])
#Apply returns to direction
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Variable assignment
endgains = 1
endreturns = 1
#Performance metric
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
#Calculate returns
for g in s['LogRet']:
    slate = endreturns * (1+-g)
    endreturns = slate
#Calculate returns
for h in s['Strategy']:
    otherslate = endgains * (1+h)
    endgains = otherslate
    
#For increased accuracy, remove first window values from TheAdvice
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Print metrics 
print(s)
print(sharpe)
print(endreturns)
print(endgains)
