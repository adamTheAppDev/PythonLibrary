"""
Spyder Editor
"""
#I must confess that this indicator can be made in a fraction of the lines used.
#However MY programming skills at this time are not strong enough.
from pandas_datareader import data
import pandas as pd
import time as t
start = t.time()
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
#start = t.time() #for timing purposes un-comment this line and lines 56-57
window = 25 #minimum practical window days is probably 5
s['NDayHigh'] = s['Adj Close'].rolling(center=False, window=window).max()
s.loc[:,'NDayHigh'] = s['NDayHigh'].fillna(0)
s.loc[:,'NDayHigh'][:window-1]  = s.loc[:,'NDayHigh'][window]
s['NDayLow'] = s['Adj Close'].rolling(center=False, window=window).min()
s.loc[:,'NDayLow'] = s['NDayLow'].fillna(0)
s.loc[:,'NDayLow'][:window-1] = s.loc[:,'NDayLow'][window]
s.loc[:,'Ranger'] = range(len(s))
k = pd.DataFrame()
derp = list(s['Adj Close'])
kk = pd.Series(derp,index = range(len(s)))
k['Adj Close'] = kk
listo = []
x = []
s = s[window:]
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
s.loc[:,'DaysPastHigh'] = s['Ranger'] - s['HighDF']
s['DaysPastLow'] = s['Ranger'] - s['LowDF']
s['AroonUp'] = ((window - s['DaysPastHigh']) / window) * 100
s['AroonDown'] = ((window - s['DaysPastLow']) / window) * 100
z = set(s['AroonUp'])
zz = set(s['AroonDown'])
z1 = sorted(z)
zz1 = sorted(zz)
z2 = [l for l in z1 if l >= 0]
zz2 = [ll for ll in zz1 if ll >= 0]
s.loc[:,'AroonUp'][s['AroonUp'] < 0] = z2[0]
s.loc[:,'AroonDown'][s['AroonDown'] < 0] = zz2[0]
s['Divergence'] = s['AroonUp'] - s['AroonDown']
#end = t.time()
#print(end-start)
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))
