"""
Spyder Editor
"""
import numpy as np
from pandas_datareader import data
import pandas as pd
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='07/01/2016', end='12/01/2016') 
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
Length = len(s['LogRet'])
Range = range(0,Length)
ADI = []
store = 0
index = s.index
a = 3 #number of days for exponential moving average window
b = 10 #numer of days for exponential moving average window
multiplierA = (2/(a+1))
multiplierB = (2/(b+1))
for i in Range:
        store = store + (s['Volume'][i] * s['CLV'][i])
        ADI.append(store)
ADISeries = pd.Series(ADI, index=index)
s['ADI'] = ADISeries
EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values
smallEMA = [EMAyesterdayA]
for i in Range:
    holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
    smallEMA.append(holder)
    EMAyesterdayA = holder
smallEMAseries = pd.Series(smallEMA[1:], index=s.index)    
largeEMA = [EMAyesterdayB]
for i in Range:
    holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
    largeEMA.append(holder1)
    EMAyesterdayB = holder1
largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
s['ADIEMAsmall'] = smallEMAseries
s['ADIEMAlarge'] = largeEMAseries
s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
s['ZeroLine'] = 0
#s[['ADI','ADIEMAsmall','ADIEMAlarge']].plot(grid=True, figsize = (8,3))
s[['Chaikin','ZeroLine']].plot(grid=True, figsize = (8,3))
