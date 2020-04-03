# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from DefRSIPredictor import DefRSIPredictor
import numpy as np
import pandas as pd
from pandas_datareader import data
#Read in data
Aggregate = pd.read_pickle('VXXAGGSHARPE0865')
#Remove duplicate columns
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Assign ticker
ticker = 'VXX'
#Read in data
#s = data.DataReader(ticker, 'yahoo', start='01/01/2007', end='01/01/2050') 
s = pd.read_pickle('VXXAdvice07_50') # this is just for testing with a graph
#Iterable
ranger = range(1,len(s)+1)
#Recursive incremental datasets
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefRSIPredictor(Aggregate, q)
#    triumph.append(result)
#    print(r)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Directional methodology
s['Regime'] = np.where(s['Advice'] > -.931066, 1, 0)
s['Regime'] = np.where(s['Advice'] < -1.240275, -1, s['Regime'])
#Apply methodology to returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Ones
endgains = 1
endreturns = 1
#Short only returns
s['ShortReturns'] = s['LogRet'] * -1
#Performance metric
sharpe = (s['Strategy'].mean()-abs(s['ShortReturns'].mean()))/s['Strategy'].std()
#Compounding returns - use .cumsum().apply(np.exp)
for g in s['LogRet']:
    slate = endreturns * (1+-g)
    endreturns = slate
for h in s['Strategy']:
    otherslate = endgains * (1+h)
    endgains = otherslate
#For increased accuracy, remove first window values from TheAdvice - graphical display
s[['ShortReturns', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Display metrics
print(s)
print(sharpe)
print(endreturns)
print(endgains)
