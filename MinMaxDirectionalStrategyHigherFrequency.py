# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimizer for a donchian trend strategy for use with a 30 minute data set

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import random as rand
import pandas as pd
from pandas import read_csv
#Assign empty data structures
Dataset = pd.DataFrame()
Dataset2 = pd.DataFrame()
Counter = 0
Empty = []
#ticker = 'UVXY'
#Number of iterations
iterations = range(0, 1000)
#Read in data
s = pd.read_csv('UVXYnew.csv')
#Timer series trimmer
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
    #Generate random param
    nday = rand.randint(3,50)
    hold = rand.randint(3,50)
    ranger = range(0, hold)      
    #Market rolling highs and lows
    s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
    s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()
    #Directional methodology
    s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
    s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)
    #For all periods in time series
    for r in ranger:
        #If previous period was -1, then make -1 // this is like a ffill(limit=n)
        s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
    #Apply position to returns
    s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
    #Returns on $1
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown stat
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
#    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraints
    if MaxDD > .6:
        continue
    #Performance metric    
    dailyreturn = s['Strategy'].mean()
    dailyvol = s['Strategy'].std()
    #Constraints
    if dailyvol == 0: 
        continue
    #Performance metric
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)
    #Add params and metrics to list
    Empty.append(nday)
    Empty.append(hold)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to Series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
#Metric of chocie    
z1 = Dataset.iloc[2]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all params
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top params
for j in v1:
      #Find column ID of param
      r = Dataset.columns[(Dataset == j).iloc[2]]    
      #Add param set to dataframe by column ID
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric
y = max(z1)
#Column of top metric
k = Dataset.columns[(Dataset == y).iloc[2]] 
#Top param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top param set
print(Dataset[k])
    
#Read in params from top param set
nday = int(Dataset[kfloat][0])
hold = int(Dataset[kfloat][1])
#Iterable
ranger = range(0, hold)
#Market rolling highest high and lowest low
s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()
#Directional methodology
s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)
#Zeros
s['OriginalTrade'] = 0
#If no trade in previous period then is original trade
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1 
#s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = -1 
#For number of iterations
for r in ranger:
    #If 1 in previous period, then add 1 like a .ffill(limit=n)
    s['Regime'] = np.where(s['Regime'].shift(1) == 1, 1, s['Regime'])

#Apply position to returns
s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
#Returns on $1
s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
#Incorrectly calculated drawdown stat
drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)
#Performance stats
dailyreturn = s['Strategy'].mean()
dailyvol = s['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
#Graphical display
s['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
