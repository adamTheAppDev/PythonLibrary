"""
Spyder Editor
"""
import numpy as np
from pandas_datareader import data
import pandas as pd
import time as t
start = t.time()
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
#start = t.time() #for timing purposes un-comment this line and lines 58-59
window = 10 #minimum window is 10 days
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['NDayHigh'] = s['Adj Close'].rolling(center=False, window=window).max()
s['NDayHigh'] = s['NDayHigh'].fillna(0)
s['NDayHigh'][:window-1]  = s.loc[:,'NDayHigh'][window]
s['NDayLow'] = s['Adj Close'].rolling(center=False, window=window).min()
s['NDayLow'] = s['NDayLow'].fillna(0)
s['NDayLow'][:window-1]  = s.loc[:,'NDayLow'][window]
s.loc[:,'Ranger'] = range(len(s))
k = pd.DataFrame()
derp = list(s['Adj Close'])
kk = pd.Series(derp,index = range(len(s)))
k['Adj Close'] = kk
listo = []
x = []
for i in s['NDayHigh']:
    x.append(i)
for xx in x:
    xxx = min(k['Adj Close'][k['Adj Close'] == xx].index)
    listo.append(xxx)
listo1 = []
y = []
for ii in s['NDayLow']:
    y.append(ii)
for yy in y:
    yyy = min(k['Adj Close'][k['Adj Close'] == yy].index)
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
for q in s['AroonUp']:
    if q < 0:
        print('There is an error, please proceed with caution')
        print('The window size with trouble is ', window)
for qq in s['AroonDown']:
    if qq < 0:
        print('There is an error, please proceed with caution')
        print('The window size with trouble is ', window)
#end = t.time()
#print(end-start)
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))
