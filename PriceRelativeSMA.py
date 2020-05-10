# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio/strategy tester with a brute force optimizer - price relative SMA signal

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Empty data structures
Empty = [] 
Counter = 0
Counter2 = 0
Dataset = pd.DataFrame() 
Portfolio = pd.DataFrame()
Portfolio2 = pd.DataFrame()

#Start timer
Start = t.time() #timer

#Iterable range
iterations = range(0,20000)

#Request data
Asset1 = YahooGrabber('UVXY')
Asset2 = YahooGrabber('SQQQ')

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    aa = rand.random() * 2 #uniformly distributed random number 0 to 2
    a = aa - 1          #a > 1 indicating long position in a
    bb = rand.random()
    #Constraint
    if bb >= .5:
        bb = 1
    else:
        bb = -1
    b = bb * (1 - abs(a))
    
    #Change c and d to 0 by default if you want to go flat
    c = 0
    d = 0
    #Generate random params
    e = rand.randint(3,25) 
    f = 1 - (rand.random()*2) 
    #Price relative
    Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']   
    #SMA of price relative
    Portfolio['PRSMA'] = Portfolio['PriceRelative'].rolling(window=e, center=False).mean()
    #Position sizing
    Asset1['Position'] = a
    #Alternative position sizing
    Asset1['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    c,a)        
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    #Alternative position sizing
    Asset2['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    d,b)
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position']) 

    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) 
    Portfolio['Asset2Pass'] = (Asset2['Pass']) 

    #Cumulative returns
    Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
    #Constraint
    if Portfolio['ReturnStream'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['ReturnStream'].cumsum().apply(np.exp) #cumulative returns
    #Incorrectly calculated max drawdown stat
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax()) #Max Drawdown calculation
    MaxDD = max(drawdown) 
    #Constraint
    if MaxDD > float(.5): 
        continue
    #Performance metric
    dailyreturn = Portfolio['ReturnStream'].mean()
    #Constraint
    if dailyreturn < .0003:
        continue
   
    #Performance metrics
    dailyvol = Portfolio['ReturnStream'].std()
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)

    #Save params and metrics to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)
    Empty.append(f)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Empty.append(len(Portfolio))
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
DS1W = pd.DataFrame() #this variable stores top params for specific dataset

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
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[6]] 
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')

#Read in params
window = int((Dataset[kfloat][4]))  
#Price relative
Portfolio2['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']   
#SMA of price relative
Portfolio2['PRSMA'] = Portfolio2['PriceRelative'].rolling(window=window, center=False).mean()
#Position sizing
Asset1['Position'] = (Dataset[kfloat][0])
#Alternative position sizing
Asset1['Position'] = np.where(Portfolio['PriceRelative'].shift(1) > Portfolio['PRSMA'].shift(1),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = (Dataset[kfloat][1])
#Alternative position sizing
Asset2['Position'] = np.where(Portfolio2['PriceRelative'].shift(1) > Portfolio2['PRSMA'].shift(1),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

#Pass individual return streams to portfolio
Portfolio2['Asset1Pass'] = Asset1['Pass']
Portfolio2['Asset2Pass'] = Asset2['Pass']

#Cumulative returns
Portfolio2['LongShort'] = Portfolio2['Asset1Pass'] + Portfolio2['Asset2Pass'] 
#Graphical display
Portfolio2['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio2['LongShort'].mean()
dailyvol = Portfolio2['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio2['Multiplier'] = Portfolio2['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown stat
drawdown2 =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())
#Display results
print(max(drawdown2))
#Top param set
print(Dataset[kfloat])
