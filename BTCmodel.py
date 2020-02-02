# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#BTC strategy model with brute force optimization, need BTC data set to run
#BTC/USD time series can be found for free on Investing.com

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from pandas import read_csv

#Number of iterations for brute force optimization
iterations = range(0, 2000)

#Can access BTC/USD time series for free on Investing.com
df = read_csv('BTCUSD.csv', sep = ',')

#Variable assignments
Empty = []
Counter = 0
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()

#Start timer
Start = t.time()

#Formatting
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

#Return calculation
df['LogRet'] = np.log(df['Adj Close']/df['Adj Close'].shift(1))
df['LogRet'] = df['LogRet'].fillna(0)

#Multiplier calculation
df['BTCmult'] = df['LogRet'].cumsum().apply(np.exp)
#Performance metrics
dailyreturn = df['LogRet'].mean()
dailyvol = df['LogRet'].std()
sharpe =(dailyreturn/dailyvol)

#Brute force optimization
for i in iterations:
    #Hi/Low window
    a = rand.randint(4,15)  
    #Threshold
    b = .85 + rand.random() * .3
    df['ndayhi'] = df['Adj Close'].shift(1).rolling(window = a).max()
    df['ndaylo'] = df['Adj Close'].shift(1).rolling(window = a).min()
    #If Adj Close higher than scaled Nday High, then long otherwise flat
    df['Signal'] = np.where(df['Adj Close'].shift(1) > (df['ndayhi'].shift(1) * b), 1, 0)
    #Apply returns to position
    df['Pass'] = df['Signal'].shift(1) * df['LogRet']
    #Strategy returns on $1
    df['StratReturns'] = df['Pass'].cumsum().apply(np.exp)
    #Performance metrics
    stratdailyreturn = df['Pass'].mean()
    stratdailyvol = df['Pass'].std()
    #Iteration counter
    Counter = Counter + 1
    #Performance constraint
    if stratdailyvol == 0:
        continue
    #Performance metrics
    stratsharpe =(stratdailyreturn/stratdailyvol)
    #Performance constraint
    if stratsharpe < sharpe:
        continue
        
    #Max drawdown calculation
    MultiplierMax = Portfolio['Multiplier'].cummax()
    Drawdown = (Portfolio['Multiplier']/MultiplierMax) - 1
    Drawdown = Drawdown.fillna(0)
    MaxDD = abs(min(Drawdown.cummin()))
    #Counter display
    print(Counter)
    #Save params and metrics
    Empty.append(a)
    Empty.append(b)
    Empty.append(stratsharpe)
    Empty.append(stratsharpe/MaxDD)
    Empty.append(stratdailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to Series
    Emptyseries = pd.Series(Empty)
    #Add to Data set
    Dataset[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 

#Get desired metric
z1 = Dataset.iloc[2]
#Find top n% percentile threshold
w1 = np.percentile(z1, 80)
#List stores the Nth percentile of top performers
v1 = []
#DF stores your parameters for specific dataset
DS1W = pd.DataFrame()
#Sort
for h in z1:
    if h > w1:
      v1.append(h)
#Add params to DF
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[2]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top param
y = max(z1)
#Column number
k = Dataset.columns[(Dataset == y).iloc[2]]
#End timer
End = t.time()
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])
kfloat = int(k[0])
#Apply top params to model
a = int((Dataset[kfloat][0]))
b = float((Dataset[kfloat][1]))    
df['ndayhi'] = df['Adj Close'].shift(1).rolling(window = a).max()
df['ndaylo'] = df['Adj Close'].shift(1).rolling(window = a).min()
df['Signal'] = np.where(df['Adj Close'].shift(1) > (df['ndayhi'].shift(1) * b), 1, 0)
#Apply regime to returns
df['Pass'] = df['Signal'].shift(1) * df['LogRet']
#Strategy multiplier on $1
df['StratReturns'] = df['Pass'].cumsum().apply(np.exp)
#Graphical display of strategy vs underlying
df[['StratReturns','BTCmult']].plot(grid=True, figsize=(8,5))
                                  
#Max drawdown calculation
StrategyMultiplierMax = Portfolio['StratReturns'].cummax()
StrategyDrawdown = (Portfolio['StratReturns']/StrategyMultiplierMax) - 1
StrategyDrawdown = StrategyDrawdown.fillna(0)
StrategyDrawdown = abs(min(StrategyDrawdown.cummin()))
print(max(StrategyDrawdown))
#Max drawdown calculation
CoinMultiplierMax = Portfolio['BTCmult'].cummax()
CoinDrawdown = (Portfolio['BTCmult']/CoinMultiplierMax) - 1
CoinDrawdown = CoinDrawdown.fillna(0)
CoinDrawdown = abs(min(CoinDrawdown.cummin()))
print(max(CoinDrawdown))

#Performance metrics
stratdailyreturn = df['Pass'].mean()
stratdailyvol = df['Pass'].std()
stratsharpe =(stratdailyreturn/stratdailyvol)
