# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:26:12 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

#Random variable params
#a random.int between 1 and 60 
#b random.int between 1 and 504
#c random between .0001 and .1
#d random between -.0001 and -.1
#e random between .0001 and .
#f random between -.0001 and -.4
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
iterations = range(0,40000)
empty = []
asone = pd.DataFrame()
start = t.time()
s = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s['LogRet'] = s['LogRet'].fillna(0)
for i in iterations:
    a = rand.randint(1,60)
    b = rand.randint(2,504)
    if a > b:
        continue
    c = (rand.random())/10
    e = (rand.random())/4
    if c > e:
        continue
    d = (rand.random())/10
    f = (rand.random())/4
    if d > f:
        continue
    s['a'] = s['Adj Close'].rolling(window=a, center=False).mean()
    s['b'] = s['Adj Close'].rolling(window=b, center=False).mean()
    s['a-b'] = s['a'] - s['b']
    s['Trend']= s['a-b']/s['Adj Close']
    s['Trend'] = s['Trend'].fillna(0)
    s['Touch'] = np.where(s['Trend'] > c, 1, 0)
    s['Touch'] = np.where(s['Trend'] < -d, -1, s['Touch'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1,
                                 s['Sustain'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                     s['Sustain'])
    s['Sustain'] = np.where(s['Trend'] > e, 0, s['Sustain'])
    s['Sustain'] = np.where(s['Trend'] < -f , 0, s['Sustain'])
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    endgains = 1
    endreturns = 1
    for m in s['LogRet']:
        slate = endreturns * (1+m)
        endreturns = slate
    for n in s['Strategy']:
        otherslate = endgains * (1+n)
        endgains = otherslate       
    if endreturns * 1.2 > endgains:
        continue
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(endreturns)
    empty.append(endgains)
    emptyseries = pd.Series(empty)
    asone[i] = emptyseries.values
    empty[:] = []
end = t.time()
z = asone.iloc[7]
w = np.percentile(z, 99)
v = [] #this variable stores the Nth percentile of top performers
u = pd.DataFrame() #this variable stores your financial advisors 
for h in z:
    if h > w:
      v.append(h)
for j in v:
      r = asone.columns[(asone == j).iloc[7]]    
      u = pd.concat([u,asone[r]], axis = 1)
y = max(z)
x = asone.columns[(asone == y).iloc[7]] #this is the column number
print(asone[x]) #this is the dataframe index based on column number
print(end-start) #run time in seconds
