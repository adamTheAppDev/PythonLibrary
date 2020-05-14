# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic/technical analysis tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from pandas_datareader import data
import pandas as pd
import numpy as np
#Assign tickers
ticker1 = '^RUT'
ticker2 = '^GSPC'

#Variable assignment
window = 20
s3 = pd.DataFrame()

#Request data
s1 = data.DataReader(ticker1, 'yahoo', start='10/1/2015', end='01/01/2050')
s2 = data.DataReader(ticker2, 'yahoo', start='10/1/2015', end='01/01/2050')

#Calculate log returns
s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1))
s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1))

#Calculate correlation
s3['Correlation'] = pd.rolling_corr(s1['Adj Close'],s2['Adj Close'], window)
#Trim time series
s3 = s3[window:]
#Graphical display
s3['Correlation'].plot(grid = True, figsize = (8,3))
