"""
Spyder Editor
"""

from pandas_datareader import data
import numpy as np
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='1/1/2010', end='01/01/2050')
a = 50 #moving average window
b = 151 #moving average window
s['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s['Small'] = s['Adj Close'].rolling(window=a, center=False).mean()
s['Large'] = s['Adj Close'].rolling(window=b, center=False).mean()
s[['Small', 'Large', 'Close']].plot(grid=True, figsize=(8, 5))
