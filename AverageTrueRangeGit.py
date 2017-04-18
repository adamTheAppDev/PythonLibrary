"""
Spyder Editor
"""
#There is value to be added for utlization in a strategy.
#I would normalize the ATR by price or some rolling price.
from pandas_datareader import data
import numpy as np
ticker = 'SPY'
s = data.DataReader(ticker, 'yahoo', start='01/01/2015', end='01/01/2050')
window = 14
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['AverageTrueRange'] = s['TrueRange'].rolling(window = window,
                                center=False).sum()
s['AverageTrueRange'] = ((s['AverageTrueRange'].shift(1)*(window-1
                             ) + s['TrueRange']) / window)
trim = (window * 2 - 1)
s = s[trim:]
s[['AverageTrueRange']].plot(grid=True, figsize=(8,3))
