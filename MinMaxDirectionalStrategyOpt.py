# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimizer for a donchian trend strategy

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
#Number of iterations
iterations = range(0, 5000)
#Request data
s = YahooGrabber(ticker)
#Time series trimmer
s = s[:-280]
#Start timer
Start = t.time()
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0) 

#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random variables
    nday = rand.randint(3,150)
    hold = rand.randint(3,150)
    ranger = range(0, hold)   
    
    #Calculate rolling market top and bottom
    s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
    s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()

    #Directional methodology
    s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
    s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)

    #Zeros
    s['OriginalTrade'] = 0
    #If directional assumption in period and no directional assumption in previous period then is original trade
    s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1 
    s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = -1 

    #ffill(limit = r)
    for r in ranger:
        s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])

    #Apply position to returns
    s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
    #Returns on $1
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    
    #Incorrectly calculated max drawdown stat
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
#    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > .6:
        continue
        
    #Performance metrics
    dailyreturn = s['Strategy'].mean()
    dailyvol = s['Strategy'].std()
    #Constraint
    if dailyvol == 0: 
        continue
    #Performance metrics
    sharpe =(dailyreturn/dailyvol)
    
    #Iteration tracking
    print(Counter)
    
    #Save params and metrics to list
    Empty.append(nday)
    Empty.append(hold)
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
z1 = Dataset.iloc[2]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset

#For all metrics
for h in z1:
    #If metric greater than threshold 
    if h > w1:
      #Add metric to list
      v1.append(h)
#For top metrics
for j in v1:
      #Get column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[2]]    
      #Add param set to dataframe by column ID
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
    
#Top metric
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[2]]
#Top param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top param set
print(Dataset[k])
    
#Read in top params
nday = int(Dataset[kfloat][0])
hold = int(Dataset[kfloat][1])
ranger = range(0, hold)

#Calculate rolling market top and bottom
s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()\
#Directional methodology

s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)
#If directional assumption in period and no directional assumption in previous period then is original trade
s['OriginalTrade'] = 0
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1 
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = -1 

#ffill(limit = r)
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
#Apply position to returns
s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
#Returns on $1
s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)

#Incorrectly calculated drawdown stat
drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)

#Performance metrics
dailyreturn = s['Strategy'].mean()
dailyvol = s['Strategy'].std()
sharpe =(dailyreturn/dailyvol)    
#Incorrectly calculated
print(MaxDD)

#Graphical display
s['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
                                     
                
