"""
Spyder Editor
"""
import numpy as np
from pandas_datareader import data
ticker = '^GSPC'
lag = 12
s = data.DataReader(ticker, 'yahoo', start='01/01/2010', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(lag)
                                  ) / s['Adj Close'].shift(lag)
s['ZeroLine'] = 0
s['Touch'] = np.where(s['RateOfChange'] < 0, 1,0) #long signal
s['Touch'] = np.where(s['RateOfChange'] > 0, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                 s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
s['Sustain'] = np.where(s['RateOfChange'] > 0.01, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['RateOfChange'] < -0.01, 0, s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] + s['Sustain']
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
Length = len(s['LogRet'])
Range = range(0,Length)
print(sharpe)
