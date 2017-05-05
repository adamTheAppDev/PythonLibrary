"""
Spyder Editor
"""
import numpy as np
from pandas_datareader import data
ticker = '^GSPC'
lag = 12
s = data.DataReader(ticker, 'yahoo', start='01/01/2017', end='01/01/2050')
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(lag)
                                  ) / s['Adj Close'].shift(lag)
s['ZeroLine'] = 0
s[['RateOfChange','ZeroLine']][lag:].plot(grid=True, figsize=(8,3))