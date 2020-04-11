# -*- coding: utf-8 -*-

"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import pandas as pd
from pandas_datareader import data
import numpy as np
import random as rand
#Assign ticker
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050')
#Number of iterations
iterations = range(0,8000)
#Empty data structures
counter = 0
empty = []
dataset = pd.DataFrame()

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Calculate ATR
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
#Calculate ADX
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
#For number of iterations
for x in iterations:
    #Generate random params
    counter = counter + 1    
    a = rand.randint(1,30)
    b = rand.random() * 2
    c = 100 - rand.random() * 200
    d = 100 - rand.random() * 200
    e = 100 - rand.random() * 200
    window = a
    #ATR + ADX calculation
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
    s['ADXmean'] = s['ADX'].mean() * b
    #Time series trimmers
    trim = (window * 2 - 1)
    s = s[trim:]
    replace = s[:trim]
    #Directional methdology
    s['Touch'] = np.where(s['DIdivergence'] < c, 1,0) #long signal
    s['Touch'] = np.where(s['DIdivergence'] > d, -1, s['Touch']) #short signal
    s['Sustain'] = 0
    s['Sustain'] = np.where(s['ADX'] >  s['ADXmean'], 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['ADX'] < s['ADXmean'], (s['Touch']*-1
                          ), s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    #Apply position to log returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Constraint
    if s['Strategy'].std() == 0:
        s = replace.append(s)        
        continue
    #Performance metric
    s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    #Constraint
    if s['sharpe'][-1] < 0.01:
        s = replace.append(s)        
        continue
    #Iteration tracking
    print(counter)
    #Save params and metric to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(s['sharpe'][-1])
    #List to series
    emptyseries = pd.Series(empty)
    #Add data
    s = replace.append(s)
    #Series to dataframe
    dataset[x] = emptyseries.values
    #Clear list
    empty[:] = []      
#Metric of choice
z1 = dataset.iloc[4]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your paramss for specific dataset
#For all metrics
for h in z1:
    #If metric greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top metrics
for j in v1:
      #Find column ID of metric
      r = dataset.columns[(dataset == j).iloc[4]]    
      #Add param set to data frame
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Top metric
y = max(z1)
#Column ID of top metric
k = dataset.columns[(dataset == y).iloc[4]]
#Top param set
print(dataset[k])
#Graphical display
#s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
