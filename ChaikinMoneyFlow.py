"""
Spyder Editor
"""
import numpy as np
from pandas_datareader import data
ticker = '^GSPC'
window = 20
s = data.DataReader(ticker, 'yahoo', start='11/01/2016', end='01/01/2050')
s['MFMultiplier'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['MFVolume'] = (s['Volume'] * s['MFMultiplier'])
s['ZeroLine'] = 0
s['CMF'] = s['MFVolume'].rolling(center=False, window=window).sum(
        )/s['Volume'].rolling(center=False, window=window).sum()
s[['CMF','ZeroLine']][window:].plot(grid=True, figsize=(8,3))
