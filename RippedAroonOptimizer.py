# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 12:21:13 2017

@author: AmatVictoriaCuramIII
"""

#This is a technical analysis tool, main calculation stolen from the depths of the internet

from pandas_datareader import data
import pandas as pd
import numpy as np
import time as t
import random as rand
ticker = '^GSPC'
dataset1 = pd.DataFrame()
empty = [] #reusable list
q = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
q['LogRet'] = q['LogRet'].fillna(0)
q['Ranger'] = range(len(q))
k = pd.DataFrame(index =  q['Ranger'])
AroonUp = []
AroonDown = []
AroonDate = []
iterations = range(0,2000)
start = t.time()
counter2 = 1
for i in iterations:
    AroonUp = []
    AroonDown = []
    AroonDate = []
    s = q
    a = rand.randint(6,10)
    b = 100 - rand.random() * 200
    c = 100 - rand.random() * 200
    d = 100 - rand.random() * 200
    e = 100 - rand.random() * 200
    tf = a
    AdjClose = q['Adj Close'].tolist()
    AdjCloseSeries = pd.Series(AdjClose)
    k['Adj Close'] = AdjCloseSeries
    Date = s['Ranger'].tolist()
    counter = tf
    while counter < len(s):
        Aroon_Up = ((k['Adj Close'][counter-tf:counter].tolist().index(max
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
        Aroon_Down = ((k['Adj Close'][counter-tf:counter].tolist().index(min
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
        AroonUp.append(Aroon_Up)
        AroonDown.append(Aroon_Down)
        AroonDate.append(Date[counter])
        counter = counter + 1
    s = s[tf:]
    AroonUpSeries = pd.Series(AroonUp, index=s.index)
    AroonDownSeries = pd.Series(AroonDown, index=s.index)
    s.loc[:,'AroonUp'] = AroonUpSeries
    s.loc[:,'AroonDown'] = AroonDownSeries
    s.loc[:,'Divergence'] = s['AroonUp'] - s['AroonDown']
    s.loc[:,'Touch'] = np.where(s['Divergence'] < b, 1, 0) #long signal
    s.loc[:,'Touch'] = np.where(s['Divergence'] > c, -1, s['Touch']) #short signal
    s.loc[:,'Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) 
    s.loc[:,'Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                            s['Sustain']) 
    s.loc[:,'Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) 
    s.loc[:,'Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1, 
                        s['Sustain'])
    s.loc[:,'Sustain'] = np.where(s['Divergence'] > d, 0, s['Sustain']) 
    s.loc[:,'Sustain'] = np.where(s['Divergence'] < e, 0, s['Sustain']) 
    s.loc[:,'Regime'] = s['Touch'] + s['Sustain']
    s.loc[:,'Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s.loc[:,'Strategy'] = s['Strategy'].fillna(0)
    if s['Strategy'].std() == 0:
        continue
    sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    endgains = 1
    endreturns = 1
    print(counter2)
    counter2 = counter2 + 1
    for g in s['LogRet']:
        slate = endreturns * (1+g)
        endreturns = slate
    for o in s['Strategy']:
        otherslate = endgains * (1+o)
        endgains = otherslate
    if endreturns > endgains:
        continue
    if sharpe < 0.01:
        continue
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns)
    empty.append(endgains)
    empty.append(sharpe)
    emptyseries1 = pd.Series(empty)
    dataset1[i] = emptyseries1.values
    empty[:] = []   
    AroonUpSeries = pd.Series()
    AroonDownSeries = pd.Series()
end = t.time()
sharpies = dataset1.iloc[7]
w1 = np.percentile(sharpies, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in sharpies:
    if h > w1:
      v1.append(h)
for j in v1:
      r = dataset1.columns[(dataset1 == j).iloc[7]]    
      DS1W = pd.concat([DS1W,dataset1[r]], axis = 1)
y2 = max(sharpies)
x2 = dataset1.columns[(dataset1 == y2).iloc[7]] #this is the column number
print(dataset1[x2]) #this is the dataframe index based on column number
print('Dataset 1 is optimized, it took',end-start, 'seconds') #run time in seconds
