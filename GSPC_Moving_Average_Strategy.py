# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:19:07 2016

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester, probably from the Yves Hilpisch Python for Finance book.
#pandas_datareader is deprecated, use YahooGrabber

import numpy as np
import pandas as pd
from pandas_datareader import data
sp500 = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
sp500['Close'].plot(grid=True, figsize=(8, 5))
sp500['42d'] = np.round(pd.rolling_mean(sp500['Close'], window=42), 2)
sp500['252d'] = np.round(pd.rolling_mean(sp500['Close'], window = 252), 2)
sp500[['Close', '42d', '252d']].tail()
sp500[['Close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
sp500['42-252'] = sp500['42d'] - sp500['252d']
sp500['42-252'].tail()
sp500['42-252'].head()
US = 1
LS = -5
sp500['Regime'] = np.where(sp500['42-252'] > US, 1, 0)
sp500['Regime'] = np.where(sp500['42-252'] < LS, -1, sp500['Regime'])
sp500['Regime'].value_counts()
sp500['Regime'].plot(lw=1.5)
sp500['Market'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500['Strategy'] = sp500['Regime'].shift(1) * sp500['Market']
sp500[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=True, 
                                                            figsize=(8, 5))
