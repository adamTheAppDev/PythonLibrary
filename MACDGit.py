"""
Spyder editor
"""
from pandas_datareader import data
import numpy as np
import pandas as pd
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='9/12/2016', end='01/01/2050')
a = 12 #number of days for exp moving average window
b = 26 #numer of days for exp moving average window
c = 9 #number of days for exp moving average window for MACD line
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
multiplierC = (2/(c+1))
Range = range(0, len(s['Adj Close']))
s['LogReturns'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
EMAyesterdayA = s['Adj Close'][0] #these prices are based off the SMA values
EMAyesterdayB = s['Adj Close'][0] #these prices are based off the SMA values
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (s['Adj Close'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (s['Adj Close'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
s['SmallEMA'] = smallEMAseries
s['LargeEMA'] = largeEMAseries
s['MACD'] = s['SmallEMA'] - s['LargeEMA']
MACDEMAyesterday = s['MACD'][0]
MACDEMA = [MACDEMAyesterday]
for i in Range:
    holder2 = (s['MACD'][i]*multiplierC) + (MACDEMAyesterday *
                                            (1-multiplierC))
    MACDEMA.append(holder2)
    MACDEMAyesterday = holder2
MACDEMAseries = pd.Series(MACDEMA[1:], index=s.index)
s['SignalLine'] = MACDEMAseries
s['FlatLine'] = 0
s[['SmallEMA', 'LargeEMA', 'Close']].plot(grid=True, figsize=(8, 5))
s[['SignalLine','MACD','FlatLine']].plot(grid=True, figsize=(8, 3))
