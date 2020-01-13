# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:23:57 2017

@author: AmatVictoriaCuramIII
"""

#This is similar to a remote signal - this is a tester with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
empty = []
asone = pd.DataFrame()
start = t.time()
iterations = range(0,1000)
s = data.DataReader('^VIX', 'yahoo', start='1/1/1900', end='01/01/2050') 
s2 = data.DataReader('^VXV', 'yahoo', start='1/1/1900', end='01/01/2050') 
s3 = data.DataReader('VXX', 'yahoo', start='1/1/1900', end='01/01/2050')
s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
s3['LogRet'] = s3['LogRet'].fillna(0)
s3['Meter'] = s['Close']/s2['Close']
s3['Meter'] = s3['Meter'].fillna(0)
s3['Meter'].plot(grid=True, figsize=(8, 5))
for i in iterations:
    a = rand.random()*2
    b = rand.random()*2
    s3['Touch'] = np.where(s3['Meter'] < a, -1, 0) # short signal
    s3['Touch'] = np.where(s3['Meter'] > b, 0, s3['Touch']) #flat signal
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0) #short
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1, #stays
                                         s3['Sustain']) #short
    s3['Sustain'] = np.where(s3['Touch'].shift(1) == 0, 0, 0) #flat
    s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 0, 0, #stays
                                         s3['Sustain']) #flat
#    s3['Sustain'] = np.where(s3['Meter'] < .8, 0, s3['Sustain']) #cover short
    s3['Regime'] = s3['Touch'] + s3['Sustain']
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3['Strategy'] = s3['Strategy'].fillna(0)
    endgains = 1
    endreturns = 1
#    returnstream = []
#    gainstream = []
    for g in s3['LogRet']:
        slate = endreturns * (1+-g)
#        returnstream.append(slate)
        endreturns = slate
    for h in s3['Strategy']:
        otherslate = endgains * (1+h)
#        gainstream.append(otherslate)
        endgains = otherslate
    if endreturns > endgains:
        continue
    empty.append(a)
    empty.append(b)
    empty.append(endreturns)
    empty.append(endgains)
    emptyseries = pd.Series(empty)
    asone[i] = emptyseries.values
    empty[:] = []
end = t.time()
z = asone.iloc[3]
w = np.percentile(z, 99.2)
v = [] #this variable stores the Nth percentile of top performers
u = pd.DataFrame() #this variable stores your financial advisors 
for i in z:
    if i > w:
      v.append(i)
for i in v:
      r = asone.columns[(asone == i).iloc[3]]    
      u = pd.concat([u,asone[r]], axis = 1)
y = max(z)
x = asone.columns[(asone == y).iloc[3]] #this is the column number
print(asone[x]) #this is the dataframe index based on column number
print(end-start)
