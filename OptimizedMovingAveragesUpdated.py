# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
#Number of iterations
iterations = range(0,40000)
#Empty data structures
empty = []
asone = pd.DataFrame()
#Start timer
start = t.time()
#Request data
s = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
s['LogRet'] = s['LogRet'].fillna(0)
#For number of iterations
for i in iterations:
    #Generate random params
    a = rand.randint(1,60)
    b = rand.randint(2,504)
    #Constraint
    if a > b:
        continue
    #Generate random params
    c = (rand.random())/10
    e = (rand.random())/4
    #Constraint
    if c > e:
        continue
    #Generate random params
    d = (rand.random())/10
    f = (rand.random())/4
    #Constraint
    if d > f:
        continue
    #Calculate SMA    
    s['a'] = s['Adj Close'].rolling(window=a, center=False).mean()
    s['b'] = s['Adj Close'].rolling(window=b, center=False).mean()
    #SMA spread
    s['a-b'] = s['a'] - s['b']
    #SMA spread in %
    s['Trend']= s['a-b']/s['Adj Close']
    s['Trend'] = s['Trend'].fillna(0)
    #Directional methodology
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
    #Apply postition to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Ones
    endgains = 1
    endreturns = 1
    #Compound returns
    for m in s['LogRet']:
        slate = endreturns * (1+m)
        endreturns = slate
    for n in s['Strategy']:
        otherslate = endgains * (1+n)
        endgains = otherslate       
    #Constraint    
    if endreturns * 1.2 > endgains:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(endreturns)
    empty.append(endgains)
    #List to series
    emptyseries  pd.Series(empty)
    #Series to dataframe
    asone[i] = emptyseries.values
    #Clear list 
    empty[:] = []
#End timer    
end = t.time()
#Metric of choice
z = asone.iloc[7]
#Threshold
w = np.percentile(z, 99)
v = [] #this variable stores the Nth percentile of top params
u = pd.DataFrame() #this variable stores your params 
#For all metrics
for h in z:
    #If greater than threshold
    if h > w:
      #Add to list  
      v.append(h)
#For top metrics
for j in v:
      #Get column ID of metric
      r = asone.columns[(asone == j).iloc[7]]    
      #Add param set to dataframe
      u = pd.concat([u,asone[r]], axis = 1)
#Top metrics    
y = max(z)
#Column ID of top param set
x = asone.columns[(asone == y).iloc[7]] 
#Top param set
print(asone[x]) 
#Timer stats 
print(end-start)
