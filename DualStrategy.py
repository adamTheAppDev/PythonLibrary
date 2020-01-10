# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:41:28 2017

@author: AmatVictoriaCuramIII
"""

#This is a two asset portfolio strategy tester from a kth fold optimization

import numpy as np
import pandas as pd
NC = pd.read_pickle('SP500NCAdviceJuly07_50')
RSI = pd.read_pickle('SP500AGGAdvice07_50')
NCOptimal = pd.read_pickle('SP500NCOptimal')
RSIOptimal = pd.read_pickle('SP500AGGOptimal')
a = NCOptimal.iloc[0]
b = NCOptimal.iloc[1]
c = RSIOptimal.iloc[0]
d = RSIOptimal.iloc[1]
trim = len(RSI) - len(NC)
NC = NC[:-9]
trim = len(RSI) - len(NC)
RSI = RSI[trim:]
both = pd.DataFrame()
both['Adj Close'] = NC['Adj Close']
both['NCAdvice'] = NC['Advice']
both['RSIAdvice']  = RSI['Advice']
both['LogRet'] = np.log(both['Adj Close']/both['Adj Close'].shift(1)) 
both['LogRet'] = both['LogRet'].fillna(0)
both['NCRegime'] = np.where(both['NCAdvice'] > a, 1, 0)
both['NCRegime'] = np.where(both['NCAdvice'] < b, -1, both['NCRegime'])
both['RSIRegime'] = np.where(both['RSIAdvice'] > c, 1, 0)
both['RSIRegime'] = np.where(both['RSIAdvice'] < d, -1, both['RSIRegime'])
both['SumRegimes'] = both['NCRegime'] + both['RSIRegime']
both['Regime'] = np.where(both['SumRegimes'] > 0, 1, 0)
both['Regime'] = np.where(both['SumRegimes'] < 0, -1, both['Regime'])
both['Strategy'] = (both['Regime']).shift(1)*both['LogRet']
both['Strategy'] = both['Strategy'].fillna(0)
both[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
sharpe = (both['Strategy'].mean()-abs(both['LogRet'].mean()))/both['Strategy'].std()
print(sharpe)
