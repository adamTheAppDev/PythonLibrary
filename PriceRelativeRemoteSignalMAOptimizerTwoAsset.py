# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio/strategy tester with a brute force optimizer

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
Counter = 0

#Start timer
Start = t.time()

#Assign tickers
Ticker1 = 'UVXY'
Ticker2 = '^VIX'
Ticker3 = '^VIX'

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

#Number of iterations for Brute Force Optimization
iterations = range(0, 3000)
#For number of iterations
for i in iterations:
    #Iteration tracking 
    Counter = Counter + 1
    #Generate random params
    a = rand.random()
    b = 1 - a
    c = rand.random()
    d = 1 - c
    e = rand.randint(3,30)
    window = int(e)
    #SMA
    Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
    #Position sizing
    Asset1['Position'] = a
    #Directional methodology
    Asset1['Signal'] = np.where(Asset3['MA'].shift(1) >
                    Asset3['Adj Close'].shift(1), 1, 0)
#    Asset1['Sustain'] =  np.where()
    Asset1['Position'] = np.where(Asset3['MA'].shift(1) >
                    Asset3['Adj Close'].shift(1), c, a)  
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    
    #Position sizing
    Asset2['Position'] = b
    #Directional methodology
    Asset2['Signal'] = np.where(Asset3['MA'].shift(1) >
                    Asset3['Adj Close'].shift(1), 1, 0) 
    Asset2['Position'] = np.where(Asset3['MA'].shift(1) >
                    Asset3['Adj Close'].shift(1), d, b) 
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) 
    #Cumulative returns 
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']) 
    #Constraint
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly caluculated max drawdown 
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.25): 
        continue
    #Performance metric
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metrics
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)
    #Save params to list
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
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
for h in z1:
    #If metric is greater than threshold
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
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[6]] 
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])

#Read in params
window = int((Dataset[kfloat][4]))
#SMA
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Read in position sizing 
Asset1['Position'] = (Dataset[kfloat][0])
#Directional methodology
Asset1['Position'] = np.where(Asset3['MA'].shift(1) >
          Asset3['Adj Close'].shift(1), Dataset[kfloat][2], Dataset[kfloat][0]) 
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Read in position sizing
Asset2['Position'] = (Dataset[kfloat][1])
#Directional methodology
Asset2['Position'] = np.where(Asset3['MA'].shift(1) >
          Asset3['Adj Close'].shift(1), Dataset[kfloat][3], Dataset[kfloat][1])
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass individual returns to portfolio
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] 
#Cumulative returns 
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated drawdown statistic
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
#Display results
print(max(drawdown2))
#Save to pickle
#pd.to_pickle(Portfolio, 'VXX:UVXY')
