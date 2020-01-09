# -*- coding: utf-8 -*-
"""
Created on Tue May  2 22:21:03 2017

@author: AmatVictoriaCuramIII
"""

#This is a summary statistic tool
#pandas_datareader is deprecated, use YahooGrabber
#Add more tickers for fun

from pandas_datareader import data
import pandas as pd
import numpy as np
tickers = ['^RUT','GLD','SOYB','JO','TLT']
returns = pd.DataFrame()
for s in tickers:
    s = data.DataReader(s, 'yahoo', start='10/1/2015', end='01/01/2050')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    returns = pd.concat([returns,s['LogRet']],axis = 1)
returns.columns = tickers
returns = returns.fillna(0)
matrix = returns.cov()
print(matrix)
