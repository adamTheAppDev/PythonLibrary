# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import random as rand
import pandas as pd

#Empty data structures
Dataset = pd.DataFrame()
Dataset2 = pd.DataFrame()
Counter = 0
Empty = []

#Assign ticker
ticker = 'UVXY'
#Request data
s = YahooGrabber(ticker)

#Start timer
start = t.time()

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Number of iterations for brute force optimization
iterations = range(0, 1000)
#For number of iterations
for i in iterations:
    #Iteration tracking 
    Counter = Counter + 1
    #Generate random params
    a = rand.randint(1,45)
    b = -1 + rand.random() * 1.5
    c = rand.randint(1,45)
    #Iterable
    ranger = range(0,c)
    #Calculate rate of change
    s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(a)
                                      ) / s['Adj Close'].shift(a)
    #Short only regime
    s['OGRegime'] = np.where(s['RateOfChange'] > b, -1, 0)
    s['Regime'] = s['OGRegime']
    #Number of signals
    numtrades = sum(s['OGRegime'])
    #Sample size constraints
    if numtrades > -200:
        continue
    #For number of periods in forward fill
    for r in ranger:
        #Forward fill
        s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Returns on $1
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    #Performance metric
    dailyreturn = s['Strategy'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metric
    dailyvol = s['Strategy'].std()
    #Constraint
    if dailyvol == 0:
        continue
    #Performance metric    
    sharpe =(dailyreturn/dailyvol)
    #Incorrectly calculated max drawdown statistic
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > .6:
        continue
    #Iteration tracking    
    print(Counter)
    #Save params and metrics to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
#Metric of choice    
z1 = Dataset.iloc[3]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list  
      v1.append(h)
#For top metrics        
for j in v1:
      #Get column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      #Add to dataframe
      DS1W = pd.concat(DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[3]] 
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
end = t.time()
#Timer stats
print(end-sart, 'seconds later')
#Top param set
print(Dataset[k])
#Number of periods in time series
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length)
#Iteration tracking
Counter = 0
#Number of iterations for optimization
iiterations = range(0, 1000)
#Holding period
hold = int(Dataet[kfloat][2])
#Iterable
ranger = range(0,hold)

#Calculate rate of change
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(Dataset[kfloat][0])
                                  ) / s['Adj Close'].shift(Dataset[kfloat][0])
#Short only regime
s['OGRegime'] = np.where(s['RateOfChange'] > Dataset[kfloat][1], -1, 0)
s['Regime'] = s['OGRegime']

#Forward fill for hold period
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
#For number of iterations
for ii in iiterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    d = rand.random()
    e = rand.random()
    #Constraint
    if d < e:
        continue
    #Generate random param
    f = rand.random()
    g = rand.random()
    #Constraint
    if f < g:
        continue
    #Generate random param
    h = rand.random()
    #Constraint
    if g < h:
        continue
    #Ones
    s['Position'] = 1
    #Alternative position sizing based on drawdown
    s['Position'][s['drawdown'] > d] = f
    s['Position'][s['drawdown'] < d] = g
    s['Position'][s['drawdown'] < e] = h
    #New position sizing
    s['NewRegime'] = s['Regime'] * s['Position']
    #Apply new position to returns
    s['NewStrategy'] = (s['NewRegime']).shift(1)*s['LogRet']  
    s['NewStrategy'].fillna(0)
    #Returns on $1
    s['NewMultiplier'] = s['NewStrategy'].cumsum().apply(np.exp) 
    #Incorrectly calculated max drawdown stat
    newdrawdown =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
    newdrawdown = newdrawdown.fillna(0)
    s['Newdrawdown'] =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
    NewMaxDD = max(newdrawdown)
    #Constraint
    if NewMaxDD > .55:
        continue
    #Performance metric
    dailyreturn = s['NewStrategy'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metric
    dailyvol = s['NewStrategy'].std()
    #Constraint
    if dailyvol == 0:
        continue
    #Performance metric    
    sharpe =(dailyreturn/dailyvol)
    #Add params and metrics to list
    print(Counter)
    Empty.append(d)
    Empty.append(e)
    Empty.append(f)
    Empty.append(g)
    Empty.append(h)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset2[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 

#Metric of choice
z2 = Dataset2.iloc[3]
#Threshold
w2 = np.percentile(z2, 80)
v2 = [] #this variable stores the Nth percentile of top params
DS2W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z2:
    #If greater than threshold
    if h > w2:
      #Add to list  
      v2.append(h)
#For top metrics        
for j in v2:
      #Get column ID of metric
      r = Dataset2.columns[(Dataset == j).iloc[3]]    
      #Add to dataframe
      DS2W = pd.concat([DS2W,Dataset[r]], axis = 1)
#Top metric    
y2 = max(z2)
#Column ID of top metric
k2 = Dataset2.columns[(Dataset2 == y2).iloc[3]] 
#Column ID of top metric - float
k2float = float(k2[0])
#End timer
end = t.time()
#Timer stats
print(end-start, 'seconds later')
#Display top param set
print(Dataset2[k2])

#Read in params
hold = int(Dataset[kfloat][2])
#Iterable 
ranger = range(0,hold)
#Calculate rate of change
s['RateOfChange'] = (s['Adj Close'] - s['Adj Close'].shift(Dataset[kfloat][0])
                                  ) / s['Adj Close'].shift(Dataset[kfloat][0])
#Short only regime
s['OGRegime'] = np.where(s['RateOfChange'] > Dataset[kfloat][1], -1, 0)
s['Regime'] = s['OGRegime']
#Forward fill for hold period
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
#Apply position to returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Ones
s['Position'] = 1
#Alternative position sizing
s['Position'][s['drawdown'] > Dataset2[k2float][0]] = Dataset2[k2float][2]
s['Position'][s['drawdown'] < Dataset2[k2float][0]] = Dataset2[k2float][3]
s['Position'][s['drawdown'] < Dataset2[k2float][1]] = Dataset2[k2float][4]
#Apply position sizing to previous regime
s['NewRegime'] = s['Regime'] * s['Position']
#Apply new position sizing to returns
s['NewStrategy'] = (s['NewRegime']).shift(1)*s['LogRet']  
s['NewStrategy'].fillna(0)
#Returns on $1
s['NewMultiplier'] = s['NewStrategy'].cumsum().apply(np.exp) 

#Incorrectly calculated max drawdown
newdrawdown =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
s['newdrawdown'] =  1 - s['NewMultiplier'].div(s['NewMultiplier'].cummax())
newdrawdown = newdrawdown.fillna(0)
NewMaxDD = max(newdrawdown)

#Number of signals
numtrades = sum(s['OGRegime'])
#Performance metrics
#dailyreturn = s['NewStrategy'].mean()
#dailyvol = s['NewStrategy'].std()
sharpe =(dailyreturn/dailyvol)
#Graphical display
s[['LogRet','NewStrategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
#Incorrectly calculated max drawdown stat
print(NewMaxDD*100, '% = Max Drawdown')
