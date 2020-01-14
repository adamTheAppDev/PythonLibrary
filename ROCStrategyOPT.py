"""
Spyder Editor
"""

#This is a strategy tester with a brute force optimizer

from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import random as rand
import pandas as pd

Dataset = pd.DataFrame()
Dataset2 = pd.DataFrame()
ticker = 'UVXY'
Counter = 0
Empty = []
s = YahooGrabber(ticker)
start = t.time()

s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

iterations = range(0, 1000)
for i in iterations:
    Counter = Counter + 1
    a = rand.randint(1,45)
    b = -1 + rand.random() * 1.5
    c = rand.randint(1,45)
    ranger = range(0,c)

    s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(a)
                                      ) / s['Adj Close'].shift(a)
    
    s['OGRegime'] = np.where(s['RateOfChange'] > b, -1, 0)
    s['Regime'] = s['OGRegime']
    numtrades = sum(s['OGRegime'])
    if numtrades > -200:
        continue
    for r in ranger:
        s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])

    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())

    dailyreturn = s['Strategy'].mean()
    if dailyreturn < .002:
        continue
    dailyvol = s['Strategy'].std()
    if dailyvol == 0:
        continue
    sharpe =(dailyreturn/dailyvol)
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp) 

    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
    MaxDD = max(drawdown)
    if MaxDD > .6:
        continue
    print(Counter)
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the w1 percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])
end = t.time()
print(end-start, 'seconds later')
print(Dataset[k])
Length = len(s['LogRet'])
Range = range(0,Length)
Counter = 0
iiterations = range(0, 1000)

hold = int(Dataset[kfloat][2])
ranger = range(0,hold)
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(Dataset[kfloat][0])
                                  ) / s['Adj Close'].shift(Dataset[kfloat][0])

s['OGRegime'] = np.where(s['RateOfChange'] > Dataset[kfloat][1], -1, 0)
s['Regime'] = s['OGRegime']
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])

for ii in iiterations:
    Counter = Counter + 1
    d = rand.random()
    e = rand.random()
    if d < e:
        continue
    f = rand.random()
    g = rand.random()
    if f < g:
        continue
    h = rand.random()
    if g < h:
        continue
    s['Position'] = 1
    s['Position'][s['drawdown'] > d] = f
    s['Position'][s['drawdown'] < d] = g
    s['Position'][s['drawdown'] < e] = h
    s['NewRegime'] = s['Regime'] * s['Position']
    s['NewStrategy'] = (s['NewRegime']).shift(1)*s['LogRet']  
    s['NewStrategy'].fillna(0)
    s['NewMultiplier'] = s['NewStrategy'].cumsum().apply(np.exp) 
    newdrawdown =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
    newdrawdown = newdrawdown.fillna(0)
    s['Newdrawdown'] =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
    NewMaxDD = max(newdrawdown)
    if NewMaxDD > .55:
        continue
    dailyreturn = s['NewStrategy'].mean()
    if dailyreturn < .002:
        continue
    dailyvol = s['NewStrategy'].std()
    if dailyvol == 0:
        continue
    sharpe =(dailyreturn/dailyvol)
    #s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
    #                                 figsize=(8,5))
   
    
#    s[['NewStrategy']].cumsum().apply(np.exp).plot(grid=True,
#                                    figsize=(8,5))
    print(Counter)
    Empty.append(d)
    Empty.append(e)
    Empty.append(f)
    Empty.append(g)
    Empty.append(h)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset2[0] = Emptyseries.values
    Dataset2[i] = Emptyseries.values
    Empty[:] = [] 
    
z2 = Dataset2.iloc[3]
w2 = np.percentile(z2, 80)
v2 = [] #this variable stores the w1 percentile of top performers
DS2W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z2:
    if h > w2:
      v2.append(h)
for j in v2:
      r = Dataset2.columns[(Dataset == j).iloc[3]]    
      DS2W = pd.concat([DS2W,Dataset[r]], axis = 1)
y2 = max(z2)
k2 = Dataset2.columns[(Dataset2 == y2).iloc[3]] #this is the column number
k2float = float(k2[0])
end = t.time()
print(end-start, 'seconds later')
print(Dataset2[k2])



hold = int(Dataset[kfloat][2])
ranger = range(0,hold)
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(Dataset[kfloat][0])
                                  ) / s['Adj Close'].shift(Dataset[kfloat][0])

s['OGRegime'] = np.where(s['RateOfChange'] > Dataset[kfloat][1], -1, 0)
s['Regime'] = s['OGRegime']
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])

s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)

s['Position'] = 1
s['Position'][s['drawdown'] > Dataset2[k2float][0]] = Dataset2[k2float][2]
s['Position'][s['drawdown'] < Dataset2[k2float][0]] = Dataset2[k2float][3]
s['Position'][s['drawdown'] < Dataset2[k2float][1]] = Dataset2[k2float][4]
s['NewRegime'] = s['Regime'] * s['Position']
s['NewStrategy'] = (s['NewRegime']).shift(1)*s['LogRet']  
s['NewStrategy'].fillna(0)

s['NewMultiplier'] = s['NewStrategy'].cumsum().apply(np.exp) 

newdrawdown =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
s['newdrawdown'] =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
newdrawdown = newdrawdown.fillna(0)


NewMaxDD = max(newdrawdown)

numtrades = sum(s['OGRegime'])
#dailyreturn = s['NewStrategy'].mean()

#dailyvol = s['NewStrategy'].std()
sharpe =(dailyreturn/dailyvol)
s[['LogRet','NewStrategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))

print(NewMaxDD*100, '% = Max Drawdown')
