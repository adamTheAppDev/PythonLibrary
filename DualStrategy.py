# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio strategy tester from a kth fold optimization

#Import modules 
import numpy as np
import pandas as pd

#Load data
NC = pd.read_pickle('SP500NCAdviceJuly07_50')
RSI = pd.read_pickle('SP500AGGAdvice07_50')
NCOptimal = pd.read_pickle('SP500NCOptimal')
RSIOptimal = pd.read_pickle('SP500AGGOptimal')

#Load params
a = NCOptimal.iloc[0]
b = NCOptimal.iloc[1]
c = RSIOptimal.iloc[0]
d = RSIOptimal.iloc[1]

#Trim data 
trim = len(RSI) - len(NC)
NC = NC[:-9]
trim = len(RSI) - len(NC)

#Variable assignment
RSI = RSI[trim:]
both = pd.DataFrame()

#Aggregating datasets
both['Adj Close'] = NC['Adj Close']
both['NCAdvice'] = NC['Advice']
both['RSIAdvice']  = RSI['Advice']

#Calculate returns
both['LogRet'] = np.log(both['Adj Close']/both['Adj Close'].shift(1)) 
both['LogRet'] = both['LogRet'].fillna(0)

#Directional methodology from normalized chaikin model
both['NCRegime'] = np.where(both['NCAdvice'] > a, 1, 0)
both['NCRegime'] = np.where(both['NCAdvice'] < b, -1, both['NCRegime'])

#Directional methodology from RSI model
both['RSIRegime'] = np.where(both['RSIAdvice'] > c, 1, 0)
both['RSIRegime'] = np.where(both['RSIAdvice'] < d, -1, both['RSIRegime'])

#Add decisions and make total directional methodology
both['SumRegimes'] = both['NCRegime'] + both['RSIRegime']
both['Regime'] = np.where(both['SumRegimes'] > 0, 1, 0)
both['Regime'] = np.where(both['SumRegimes'] < 0, -1, both['Regime'])

#Apply returns to directional methodology
both['Strategy'] = (both['Regime']).shift(1)*both['LogRet']
both['Strategy'] = both['Strategy'].fillna(0)

#Graphical display
both[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
#Performance metric
sharpe = (both['Strategy'].mean()-abs(both['LogRet'].mean()))/both['Strategy'].std()
print(sharpe)
