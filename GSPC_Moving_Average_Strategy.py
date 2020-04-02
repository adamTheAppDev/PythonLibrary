# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester, probably from the Yves Hilpisch Python for Finance book.
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
import pandas as pd
from pandas_datareader import data

#Request data
sp500 = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
#Graphical display
sp500['Close'].plot(grid=True, figsize=(8, 5))
#SMA calculations
sp500['42d'] = np.round(pd.rolling_mean(sp500['Close'], window=42), 2)
sp500['252d'] = np.round(pd.rolling_mean(sp500['Close'], window = 252), 2)
#Display data
sp500[['Close', '42d', '252d']].tail()
#Graphical display
sp500[['Close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
#SMA difference
sp500['42-252'] = sp500['42d'] - sp500['252d']
#Display data
sp500['42-252'].tail()
sp500['42-252'].head()
#Variable assignment for directional methodology
US = 1
LS = -5
#Directional methodology
sp500['Regime'] = np.where(sp500['42-252'] > US, 1, 0)
sp500['Regime'] = np.where(sp500['42-252'] < LS, -1, sp500['Regime'])
#Num signals
sp500['Regime'].value_counts()
sp500['Regime'].plot(lw=1.5)
#Market returns - log returns 
sp500['Market'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
#Strategy returns
sp500['Strategy'] = sp500['Regime'].shift(1) * sp500['Market']
#Graph returns
sp500[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=True, 
                                                            figsize=(8, 5))
