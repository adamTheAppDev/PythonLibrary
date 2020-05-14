# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a portfolio strategy tool with brute force optimizer
#Takes 2 assets to examine and a third for signal generation
#Use YahooGrabber for data instead of read_pickle

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabbr import YahooGrabber
#Empty data structures
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
#Start timer
Start = t.time()
#Iteration tracking
Counter = 0

#Assign tickers
#Ticker1 = 'UVXY'
#Ticker2 = '^VIX'
#Ticker3 = '^VXV'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = YahooGrabber(Ticker3)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Match lengths
Asset3 = Asset3[-len(Asset2):]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
#Price relative
Asset3['Contango'] = (Asset2['Close']/Asset3['Close'])

#Number of iterations for Brute Force Optimization
iterations = range(0, 2000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a = rand.random()
    b = 1 - a
    c = rand.random()
    d = 1 - c
    e = 1.5 - (rand.random()*.5)
    
    #Position sizing
    Asset1['Position'] = a
    #Alternative position sizing
    Asset1['Position'] = np.where(Asset3['Contango'].shift(1) > e,
                                    c,a)   
    #Apply position to return stream
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing 
    Asset2['Position'] = b
    #Alternative position sizing
    Asset2['Position'] = np.where(Asset3['Contango'].shift(1) > e,
                                    d,b)
    #Apply position to return stream        
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    
    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1)
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)

    #Cumulative returns
    Portfolio['TotalRet'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass'])
    #Constraint
    if Portfolio['TotalRet'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['TotalRet'].cumsum().apply(np.exp)
    
    #Incorrectly calculated max drawdown
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraints
    if MaxDD > float(.3): 
        continue
    #Performance metric
    dailyreturn = Portfolio['TotalRet'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metric
    dailyvol = Portfolio['TotalRet'].std()
    
    #Performance metric
    sharpe = (dailyreturn / dailyvol)
    
    #Iteration tracking
    print(Counter)
    
    #Add params and metrics to lsit
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)
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
z1 = Dataset.iloc[6]
#Threshold 
w1 = np.percentile(z1, 80)
v1 = [] #this list stores top Nth percentile of metrics
DS1W = pd.DataFrame() #this variable stores top params sets
#For all metrics
for h in z1: 
    #If greater than threshold
    if h > w1: 
      #Add to list  
      v1.append(h)
#For top metrics        
for j in v1: 
      #Get column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[6]] 
      #Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1) 
#Top metric    
y = max(z1)
#Column ID of top param set
k = Dataset.columns[(Dataset == y).iloc[6]] 
#Column ID of top param set - float
kfloat = float(k[0]) 
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top metric
print(Dataset[k])

#Read in top params
#Position sizing
Asset1['Position'] = (Dataset[kfloat][0])
#Alternative position sizing
Asset1['Position'] = np.where(Asset3['Contango'].shift(1) > Dataset[kfloat][4],
                                    Dataset[kfloat][2],Dataset[kfloat][0])
#Apply position to returns 
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = (Dataset[kfloat][1])
#Alternative position sizing
Asset2['Position'] = np.where(Asset3['Contango'].shift(1) > Dataset[kfloat][4],
            Dataset[kfloat][3],Dataset[kfloat][1])
#Apply position to returns 
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

#Pass individual metrics to return stream
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Cumulative returns
Portfolio['TotalRet'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
Portfolio['TotalRet'][:].cumsum().apply(np.exp).plot(grid=True, figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['TotalRet'].mean()
dailyvol = Portfolio['TotalRet'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['TotalRet'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown statistic
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#print('Max drawdown is about ' + str(round((max(drawdown2)*100),2)) +'%')
