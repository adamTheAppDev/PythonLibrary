# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

#BTC strategy model with brute force optimization, need BTC data set to run. 

import numpy as np
import random as rand
import pandas as pd
import time as t
from pandas import read_csv
iterations = range(0, 2000)
df = read_csv('BTCUSD.csv', sep = ',')
Empty = []
Counter = 0
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
df = df.set_index('Date')
df = df.iloc[::-1] 
df['Adj Close'] = df['Adj Close'].str.replace(',', '')
df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
df['High'] = df['High'].str.replace(',', '')
df['High'] = pd.to_numeric(df['High'], errors='coerce')
df['Open'] = df['Open'].str.replace(',', '')
df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
df['Low'] = df['Low'].str.replace(',', '')
df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
df['LogRet'] = np.log(df['Adj Close']/df['Adj Close'].shift(1))
df['LogRet'] = df['LogRet'].fillna(0)
df['BTCmult'] = df['LogRet'].cumsum().apply(np.exp)
dailyreturn = df['LogRet'].mean()
dailyvol = df['LogRet'].std()
sharpe =(dailyreturn/dailyvol)

for i in iterations:
    a = rand.randint(4,15)  
    b = .85 + rand.random() * .3
    df['ndayhi'] = df['Adj Close'].shift(1).rolling(window = a).max()
    df['ndaylo'] = df['Adj Close'].shift(1).rolling(window = a).min()
    df['Signal'] = np.where(df['Adj Close'].shift(1) > (df['ndayhi'].shift(1) * b), 1, 0)
    df['Pass'] = df['Signal'].shift(1) * df['LogRet']
    df['StratReturns'] = df['Pass'].cumsum().apply(np.exp)
    stratdailyreturn = df['Pass'].mean()
    stratdailyvol = df['Pass'].std()
    Counter = Counter + 1
    if stratdailyvol == 0:
        continue
    stratsharpe =(stratdailyreturn/stratdailyvol)
    if stratsharpe < sharpe:
        continue
    drawdown =  1 - df['StratReturns'].div(df['StratReturns'].cummax())
    MaxDD = (max(drawdown))
    print(Counter)
    Empty.append(a)
    Empty.append(b)
    Empty.append(stratsharpe)
    Empty.append(stratsharpe/MaxDD)
    Empty.append(stratdailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 

z1 = Dataset.iloc[2]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[2]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[2]] #this is the column number
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])
kfloat = int(k[0])
a = int((Dataset[kfloat][0]))
b = float((Dataset[kfloat][1]))    
df['ndayhi'] = df['Adj Close'].shift(1).rolling(window = a).max()
df['ndaylo'] = df['Adj Close'].shift(1).rolling(window = a).min()
df['Signal'] = np.where(df['Adj Close'].shift(1) > (df['ndayhi'].shift(1) * b), 1, 0)
df['Pass'] = df['Signal'].shift(1) * df['LogRet']
df['StratReturns'] = df['Pass'].cumsum().apply(np.exp)

df[['StratReturns','BTCmult']].plot(grid=True,    figsize=(8,5))
                                  
drawdown =  1 - df['StratReturns'].div(df['StratReturns'].cummax())
print(max(drawdown))
drawdown2 =  1 - df['BTCmult'].div(df['BTCmult'].cummax())
print(max(drawdown2))

stratdailyreturn = df['Pass'].mean()
stratdailyvol = df['Pass'].std()
stratsharpe =(stratdailyreturn/stratdailyvol)
