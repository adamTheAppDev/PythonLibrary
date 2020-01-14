# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:03:41 2018

@author: AmatVictoriaCuramIII
"""

#This is a two asset portfolio/strategy tester with a brute force optimizer - price relative SMA signal

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
iterations = range(0,20000)


Empty = [] #list
Start = t.time() #timer
Counter = 0
Counter2 = 0
Dataset = pd.DataFrame() #Extra DataFrame
Portfolio = pd.DataFrame()
Portfolio2 = pd.DataFrame()
Asset1 = YahooGrabber('UVXY')
Asset2 = YahooGrabber('SQQQ')

#log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#match length
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

for i in iterations:
    Counter = Counter + 1
    aa = rand.random() * 2 #uniformly distributed random number 0 to 2
    a = aa - 1          #a > 1 indicating long position in a
    bb = rand.random()
    if bb >= .5:
        bb = 1
    else:
        bb = -1
    b = bb * (1 - abs(a))
    
    #you can change c and d to 0 by default if you want to just go flat
    c = 0
    d = 0
#    cc = rand.random() * 2 #uniformly distributed random number 0 to 2
#    c = cc - 1          #cc > 1 indicating long position in c
#    dd = rand.random() * 2
#    if dd >= 1:
#        edd = 1
#    else:
#        edd = -1
#    d = (dd - 1)
#    if abs(c) + abs(d) > 1:
#        continue
    e = rand.randint(3,25) 
    f = 1 - (rand.random()*2) 

    Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']   
    Portfolio['PRSMA'] = Portfolio['PriceRelative'].rolling(window=e, center=False).mean()
    
#    Asset1['SMA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
#    Asset2['SMA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    c,a)                                    
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position']) #position size * returns

    Asset2['Position'] = b
    Asset2['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    d,b)
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position']) #position size * returns

    #Pass individual adjusted return streams to dual asset portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) 
    Portfolio['Asset2Pass'] = (Asset2['Pass']) 

    #Add to make dual asset portfolio
    Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 

    if Portfolio['ReturnStream'].std() == 0:    
        continue
    
    Portfolio['Multiplier'] = Portfolio['ReturnStream'].cumsum().apply(np.exp) #cumulative returns
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax()) #Max Drawdown calculation
    MaxDD = max(drawdown) 
    if MaxDD > float(.5): 
        continue
    
    dailyreturn = Portfolio['ReturnStream'].mean()
    if dailyreturn < .0003:
        continue
   
    #statistics
    dailyvol = Portfolio['ReturnStream'].std()
    sharpe =(dailyreturn/dailyvol)
    MaxDD = max(drawdown)
    print(Counter)

    #save parameters for further analysis
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)
    Empty.append(f)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
#    Empty.append(m[0])
#    Empty.append(m[1])
    Empty.append(len(Portfolio))
    
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
#find optimal parameters from pair
z1 = Dataset.iloc[6] #large row of specific statistic
w1 = np.percentile(z1, 80) #nth percentile of specific statistic
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores top parameters for specific dataset

#populate v1 to make DS1W
for h in z1:
    if h > w1:
      v1.append(h)

#populate DS1W with parameters
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[6]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)

#find 'optimal' parameters for model and pass to Dataset2
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[6]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
window = int((Dataset[kfloat][4]))  

Portfolio2['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']   
Portfolio2['PRSMA'] = Portfolio2['PriceRelative'].rolling(window=window, center=False).mean()

Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Position'] = np.where(Portfolio2['PriceRelative'].shift(1) > Portfolio2['PRSMA'].shift(1),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])


Portfolio2['Asset1Pass'] = Asset1['Pass']
Portfolio2['Asset2Pass'] = Asset2['Pass']
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
Portfolio2['LongShort'] = Portfolio2['Asset1Pass'] + Portfolio2['Asset2Pass'] 
Portfolio2['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Portfolio2['LongShort'].mean()
dailyvol = Portfolio2['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio2['Multiplier'] = Portfolio2['LongShort'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
print(max(drawdown2))
print(Dataset[kfloat])
