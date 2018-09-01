# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 23:32:44 2017

@author: AmatVictoriaCuramIII
"""

from DefModADXAdviceGiver import DefModADXAdviceGiver
import numpy as np
import pandas as pd
from pandas_datareader import data
Aggregate = pd.read_pickle('RUTModADXAGGSHARPE065')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
ticker = '^RUT'
#s = data.DataReader(ticker, 'yahoo', start='01/01/1994', end='01/01/2007') 
s = pd.read_pickle('RUTModADXAGGAdviceColumn94_07') # this is just for testing with a graph
#s2 = pd.DataFrame({'Open':[1419.57],'High':[1423.52],'Low':[1413.68],'Close':[0],'Volume':[0],
#'Adj Close':[1417.51]},index = ['2017-04-27 00:00:00']) #interday
#s = pd.concat([s,s2],axis = 0)
#ranger = range(1,len(s)+1)
#dictionary = { r : s.loc[s.index[:r],:] for r in ranger}
#triumph = []
#for r in ranger:
#    q = dictionary[r]
#    result = DefModADXAdviceGiver(Aggregate, q)
#    triumph.append(result)  
#    print(r)
#    print(result)
#TheAdvice = pd.Series(triumph, index=s.index)
#s['Advice'] = TheAdvice
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Regime'] = np.where(s['Advice'] > -1.969, 1, 0)
s['Regime'] = np.where(s['Advice'] < -1.562601, -1, s['Regime'])
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
endgains = 1
endreturns = 1
s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
for g in s['LogRet']:
    slate = endreturns * (1+-g)
    endreturns = slate
for h in s['Strategy']:
    otherslate = endgains * (1+h)
    endgains = otherslate
#For increased accuracy, remove first window values from TheAdvice
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
print(s)
print(s['sharpe'][-1])
print(endreturns)
print(endgains)