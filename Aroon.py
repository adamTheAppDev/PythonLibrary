"""
Spyder Editor
"""
#the following code runs, but it has major flaws for when multiple days have similar closing prices.. to be continued..
import numpy as np
from pandas_datareader import data
import pandas as pd
import time as t
start = t.time()
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
#start = t.time() #for timing purposes un-comment this line and lines 48-49
window = 25 #minimum functional window is 10 days
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['NDayHigh'] = s['Adj Close'].rolling(center=False, window=window).max()
s['NDayHigh'] = s['NDayHigh'].fillna(0)
s['NDayHigh'][:window-1]  = s.loc[:,'NDayHigh'][window]
s['NDayLow'] = s['Adj Close'].rolling(center=False, window=window).min()
s['NDayLow'] = s['NDayLow'].fillna(0)
s['NDayLow'][:window-1]  = s.loc[:,'NDayLow'][window]
s.loc[:,'Ranger'] = range(len(s))
k = pd.DataFrame(index = s['Adj Close'])
k['Ranger'] = range(len(s))
listo = []
x = []
for i in s['NDayHigh']:
    x.append(i)
for xx in x:
    xxx = k.loc[xx,'Ranger']
    listo.append(xxx)
listo1 = []
y = []
for ii in s['NDayLow']:
    y.append(ii)
for yy in y:
    yyy = k.loc[yy,'Ranger']
    listo1.append(yyy)
HighIndex = pd.Series(listo,index=s.index)
LowIndex = pd.Series(listo1,index=s.index)
HighDF = pd.DataFrame(HighIndex,columns = ['HighDF'])
LowDF = pd.DataFrame(LowIndex,columns = ['LowDF'])
s = pd.concat([s, HighDF, LowDF], axis = 1)
s['DaysPastHigh'] = s['Ranger'] - s['HighDF']
s['DaysPastLow'] = s['Ranger'] - s['LowDF']
s['AroonUp'] = ((window - s['DaysPastHigh']) / window) * 100
s['AroonDown'] = ((window - s['DaysPastLow']) / window) * 100
s = s[window:]
#end = t.time()
#print(end-start)
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))
