# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio/stretegy tester with a brute force optimizer

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Empty data structures
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Assign tickers
Ticker1 = 'TQQQ'
Ticker2 = 'TMF'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Out of sample trim        
Asset1 = Asset1[-60:]
Asset2 = Asset2[-60:]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Number of iterations for Brute Force Optimization
iterations = range(0, 4000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a = rand.random()
    b = 1 - a
    #Position sizing // apply position to returns
    Asset1['Position'] = a
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass'])
    #Cumulative returns
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']) 
    #    Portfolio['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                         figsize=(8,5))  
    #Constraint
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown statistic
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
#    if MaxDD > float(.35): 
#        continue
    #Performance metric
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
#    if dailyreturn < .00015:
#        continue
    #Performance metrics
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Iteration tracking
    print(Counter)
    #Generate random params
    Empty.append(a)
    Empty.append(b)
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
      #Get column ID
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      #Add to dataframe 
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[3]]
#Column ID of top metic as float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])

#Read in params
#Position sizing // apply position to returns
Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass individual return streams to portfolio
Portfolio['Asset1Pass'] = Asset1['Pass'] #* (-1)
Portfolio['Asset2Pass'] = Asset2['Pass']
#Pass returns to portfolio
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance statistics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown stat
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
print(max(drawdown2))
