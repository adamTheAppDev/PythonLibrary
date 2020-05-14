# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a techincal analysis tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
#Assign ticker
ticker = '^GSPC'
#Variable assignment
lag = 12
#Request data
s = data.DataReader(ticker, 'yahoo', start='01/01/2017', end='01/01/2050')
#Calculate rate of change
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(lag)
                                  ) / s['Adj Close'].shift(lag)
#Horizontal line
s['ZeroLine'] = 0
#Graphical display
s[['RateOfChange','ZeroLine']][lag:].plot(grid=True, figsize=(8,3))
