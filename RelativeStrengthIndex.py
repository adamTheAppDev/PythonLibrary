"""
Spyder editor
"""
import numpy as np
from pandas_datareader import data
s1 = data.DataReader('^GSPC', 'yahoo', start='01/01/2015', end='01/01/2050') 
s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1)) 
s1['LogRet'] = s1['LogRet'].fillna(0)
closeprice = s1['Adj Close']
window = 14  
change = closeprice.diff()
change = change[1:]
up, down = change.copy(), change.copy()
up[up < 0] = 0
down[down > 0] = 0
AvgGain = up.rolling(window).mean()
AvgGain = AvgGain.fillna(0)
AvgLoss = down.abs().rolling(window).mean()
AvgLoss = AvgLoss.fillna(0)
RS = AvgGain/AvgLoss
RS = RS.fillna(0)
RSI = 100 - (100/(1.0+RS))
RSI = RSI[window:]
RSI.plot(grid=True, figsize=(8,3))
