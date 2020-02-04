# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy optimizer

#Import modules
import pandas as pd
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import random as rand

#Input ticker
ticker = '^GSPC'

#Request data - Use YahooGrabber
s = YahooGrabber(ticker)
#Number of iterations for brute force optimizer
iterations = range(0,800)

#Loop counter
counter = 0

#Empty assignments
empty = []
dataset = pd.DataFrame()

#Start timer
start = t.time()

#Return calculation
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#ATR calculation
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)

#First part of ADX calculation
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)

#For number of iterations
for x in iterations:
    #Loop counter
    counter = counter + 1
    
    #Pass random params
    a = rand.randint(1,30)
    b = 100 - rand.random() * 200
    c = 100 - rand.random() * 200
    d = 100 - rand.random() * 200
    e = 100 - rand.random() * 200
    
    #ADX calculations
    window = a
    s['AverageTrueRange'] = s['TrueRange'].rolling(window = window,
                                    center=False).sum()
    s['AverageTrueRange'] = ((s['AverageTrueRange'].shift(1)*(window-1
                                 ) + s['TrueRange']) / window)
    s['SmoothPDM'] = s['PDM'].rolling(window = window,
                                    center=False).sum()
    s['SmoothPDM'] = ((s['SmoothPDM'].shift(1)*(window-1
                                 ) + s['PDM']) / window)
    s['SmoothMDM'] = s['MDM'].rolling(window = window,
                                    center=False).sum()
    s['SmoothMDM'] = ((s['SmoothMDM'].shift(1)*(window-1
                                 ) + s['MDM']) / window)
    s['PDI'] = (100*(s['SmoothPDM']/s['AverageTrueRange']))
    s['MDI'] = (100*(s['SmoothMDM']/s['AverageTrueRange']))
    s['DIdiff'] = abs(s['PDI'] - s['MDI'])
    s['DIdivergence'] = s['PDI'] - s['MDI']
    s['DIsum'] = s['PDI'] + s['MDI']
    s['DX'] = (100 * (s['DIdiff']/s['DIsum']))
    s['DX'] = s['DX'].fillna(0)
    s['ADX'] = s['DX'].rolling(window = window, center = False).mean()
    s['ADXmean'] = s['ADX'].mean()
    
    #Directional methodology
    s['Touch'] = np.where(s['DIdivergence'] < b, 1,0) #long signal
    s['Touch'] = np.where(s['DIdivergence'] > c, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                     s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                     s['Sustain']) 
    s['Sustain'] = np.where(s['DIdivergence'] > d, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['DIdivergence'] < e, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    
    #Skip parameters if no positions taken
    if s['Strategy'].std() == 0:    
        continue
    #Performance metrics
    s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    #Performance filter to keep better parameter sets
    if s['sharpe'][-1] < 0.01:     
        continue
    #Performance filter based on final returns to keep better parameter sets (could be a misleading metric)
    if s['LogRet'].cumsum().apply(np.exp)[-1] > s['Strategy'].cumsum(
                            ).apply(np.exp)[-1]:     
        continue                                
    #Loop counter
    print(counter)
    
    #Save parameters and performance metrics to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(s['sharpe'][-1])
    
    #List to Series
    emptyseries = pd.Series(empty)
    #Series to DataFrame
    dataset[x] = emptyseries.values
    #Clear list for next iteration
    empty[:] = []      
#Series of performance metrics
z1 = dataset.iloc[5]
#Find nth percentile threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of desirable parameters
DS1W = pd.DataFrame() #this variable stores your parameters for specific dataset
#For all performance metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add metric to list
      v1.append(h)
#For all the metrics greater than threshold
for j in v1:
      #Find column numbers of corresponding metric
      r = dataset.columns[(dataset == j).iloc[5]] 
      #Add parameters to DataFrame by column number
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Find the TOP performance metric
y = max(z1)
#Find column name that belongs to top metric
k = dataset.columns[(dataset == y).iloc[5]] #this is the column number
#End timer
end = t.time()
print(end-start, 'seconds later')
#Output TOP parameters
print(dataset[k])
#Graphical display
#s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
