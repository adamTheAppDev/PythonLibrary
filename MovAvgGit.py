# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pandas_datareader import data
import numpy as np
s = data.DataReader('^GSPC', 'yahoo', start='1/1/2010', end='01/01/2050')
s['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s['Small'] = s['Adj Close'].rolling(window=56, center=False).mean()
s['Large'] = s['Adj Close'].rolling(window=151, center=False).mean()
s[['Small', 'Large', 'Close']].plot(grid=True, figsize=(8, 5))