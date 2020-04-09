# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
from DefNCAdviceGiver import DefNCAdviceGiver
import numpy as np
import pandas as pd
from pandas_datareader import data

#Read in data
Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Assign ticker
ticker = '^GSPC'
#Read in data
#s = data.DataReader(ticker, 'yahoo', start='07/01/2007', end='01/01/2050') 
s = pd.read_pickle('SP500NCAdviceJuly07_50') # this is just for testing with a graph
#Iterable
ranger = range(1,len(s)+1)
#Incrementally longer time series
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefNCAdviceGiver(Aggregate, q)
#    triumph.append(result)
#    print(r)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Directional methodology
s['Regime'] = np.where(s['Advice'] > .875601, 1, 0)
s['Regime'] = np.where(s['Advice'] < .548866, -1, s['Regime'])
#Apply position to returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Ones
endgains = 1
endreturns = 1
#Performance metrics
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
#Compound returns
for g in s['LogRet']:
    slate = endreturns * (1+-g)
    endreturns = slate
for h in s['Strategy']:
    otherslate = endgains * (1+h)
    endgains = otherslate

#Graphical display
#For increased accuracy, remove first window values from TheAdvice
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Display results
print(s)
print(sharpe)
print(endreturns)
print(endgains)
