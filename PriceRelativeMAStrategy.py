# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a 2 asset portfolio analysis tool

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

#Price Relative Moving Average Strategy

#Input tickers
Ticker1 = 'UVXY'
Ticker2 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)

#Match time series lengths
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

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
    d = rand.random()
    #Constraints
    if c + d > 1:
        continue
    #Generate random params 
    e = rand.randint(3,20)
    window = int(e)
    #Position sizing
    Asset1['Position'] = a
    #Directional methodology
    Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    c,a)
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    #Directional methodology
    Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    d,b)
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Pass returns to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
    #Combine returns
    Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
    #Constraints
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Muliplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.1): 
        continue
    #Performance metric
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
    if dailyreturn < .003:
        continue
    #Performance metric
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Incorrectly calculated
    MaxDD = max(drawdown)
    #Iteration tracking
    print(Counter)
    #Save params and metrics to list
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
      #Add param set to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[6]]
#Top param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top param set
print(Dataset[k])

#Read in top params
window = int((Dataset[kfloat][4]))
#Calculate SMA
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()   
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset1['Position'] = (Dataset[kfloat][0])
#Directional methodology
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = (Dataset[kfloat][1])
#Directional methodology
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass returns to portfolio
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Combine returns
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
#Incorrectly calculated max drawdown statistic
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
print(max(drawdown2))
#pd.to_pickle(Portfolio, 'VXX:UVXY')
