# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is similar to a remote signal - this is a tester with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
#Empty structures
empty = []
asone = pd.DataFrame()
start = t.time()
#Number of iterations
iterations = range(0,1000)
#Request data
s = data.DataReader('^VIX', 'yahoo', start='1/1/1900', end='01/01/2050') 
s2 = data.DataReader('^VXV', 'yahoo', start='1/1/1900', end='01/01/2050') 
s3 = data.DataReader('VXX', 'yahoo', start='1/1/1900', end='01/01/2050')
#Calculate log returns
s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
s3['LogRet'] = s3['LogRet'].fillna(0)
#Price relative
s3['Meter'] = s['Close']/s2['Close']
s3['Meter'] = s3['Meter'].fillna(0)
#PR graphical display
s3['Meter'].plot(grid=True, figsize=(8, 5))
#For all iterations
for i in iterations:
    #Generate random params
    a = rand.random()*2
    b = rand.random()*2
    #Directional methodology
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
    #Apply position to returns
    s3['Strategy'] = (s3['Regime']).shift(1)*s3['LogRet']
    s3['Strategy'] = s3['Strategy'].fillna(0)
    #Ones
    endgains = 1
    endreturns = 1
#    returnstream = []
#    gainstream = []
    #Compound returns 
    for g in s3['LogRet']:
        slate = endreturns * (1+-g)
#        returnstream.append(slate)
        endreturns = slate
    for h in s3['Strategy']:
        otherslate = endgains * (1+h)
#        gainstream.append(otherslate)
        endgains = otherslate
    #Constraint
    if endreturns > endgains:
        continue
    #Save params and metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(endreturns)
    empty.append(endgains)
    #List to series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    asone[i] = emptyseries.values
    #Clear list
    empty[:] = []
#End timer    
end = t.time()
#Metric of choice
z = asone.iloc[3]
#Threshold
w = np.percentile(z, 99.2)
v = [] #this variable stores the Nth percentile of top params
u = pd.DataFrame() #this variable stores your params 
#For all metrics
for i in z:
    #If greater than threshold
    if i > w:
      #Add to list  
      v.append(i)
#For top metrics        
for i in v:
      #Get column ID of metric
      r = asone.columns[(asone == i).iloc[3]]    
      #Add param set to dataframe  
      u = pd.concat([u,asone[r]], axis = 1)
#Top metric    
y = max(z)
#Column ID of top metric
x = asone.columns[(asone == y).iloc[3]] 
#Top param set
print(asone[x])
#Timer stats
print(end-start)
