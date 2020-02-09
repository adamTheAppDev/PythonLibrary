# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a single issue strategy tester
#Tests one asset at a time, finds optimal params

#Load modules
import numpy as np
import random as rand
import pandas as pd
import time as tt
from DatabaseAgeScanner import DatabaseAgeScanner
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
import os
#Preliminary assignment

Empty = [] #list
Start = tt.time() #timer
Counter = 0
Counter2 = 0
iterations = range(0, 1000) #Loop size
Dataset2 = pd.DataFrame() #Extra DataFrame

#Input
tickers = DatabaseAgeScanner(1250)
tickers = tickers[:]
#tickers = ('AA', 'AAME', 'AAN', 'AAON', 'AAPL', 'AB', 'ABAX', 'ABC', 'ABCB', 'ABEO', 'ABEV')


#Choose number of asset pairs in final equal weighted portfolio
listlen = len(tickers)
desiredlen = 10
lenthreshold = abs(int(round((1 -(((desiredlen)/listlen) - .0000001) * 100))))

Portfolio = pd.DataFrame()
#Here we go

#Brute Force Optimization
for t in tickers: #Every pair in pairlist
    try:
        #Preliminary set up and 
        Ticker1 = t
        Dataset = pd.DataFrame()
        Asset1 = YahooGrabber(Ticker1)
    #Get log returns
        Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
        Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
  
    #Run random variables through model and acquire parameters  
        for i in iterations:
#            Counter = Counter + 1
            #SMA lookback window            
            a = rand.randint(3,252)
    
            

            #SMA calculation            
            Asset1['SMA'] = Asset1['Adj Close'].rolling(window=a, center=False).mean()     
            
            #fixed size position for a and b, alternative fixed positions of c and d 
            
            Asset1['Position'] = 0
            Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['SMA'].shift(1),
                                            1,-1)                                    
            Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position']) #position size * returns

            if Asset1['Pass'].std() == 0:    
                continue
                
            #Returns on 1$
            Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp) #cumulative returns
            
            #Max drawdown calculation
            MultiplierMax = Asset1['Multiplier'].cummax()
            Drawdown = (Asset1['Multiplier']/MultiplierMax) - 1
            Drawdown = Drawdown.fillna(0)
            MaxDD = abs(min(Drawdown.cummin()))
            
            #Return constraints
            dailyreturn = Asset1['Pass'].mean()
#            if dailyreturn < .0003:
#                continue
           
            #Statistics
            dailyvol = Asset1['Pass'].std()
            sharpe =(dailyreturn/dailyvol)
            MaxDD = max(drawdown)
#            print(Counter)

            #Save parameters for further analysis
            Empty.append(a)
            Empty.append(sharpe)
            Empty.append(sharpe/MaxDD)
            Empty.append(dailyreturn/MaxDD)
            Empty.append(dailyreturn)            
            Empty.append(MaxDD)
            Empty.append(t)
            Empty.append(len(Asset1['Pass']))
            
            Emptyseries = pd.Series(Empty)
            Dataset[0] = Emptyseries.values
            Dataset[i] = Emptyseries.values
            Empty[:] = [] 
    #Find optimal parameters from pair
        z1 = Dataset.iloc[2] #large row of specific statistic
        w1 = np.percentile(z1, 80) #nth percentile of specific statistic
        v1 = [] #this variable stores the Nth percentile of top performers
        DS1W = pd.DataFrame() #this variable stores top parameters for specific dataset

        #Populate v1 to make DS1W
        for h in z1:
            if h > w1:
              v1.append(h)

        #Populate DS1W with parameters
        for j in v1:
              r = Dataset.columns[(Dataset == j).iloc[2]]    
              DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
        
        #Find 'optimal' parameters for model and pass to Dataset2
        y = max(z1)
        k = Dataset.columns[(Dataset == y).iloc[2]] #this is the column number
        kfloat = float(k[0])
        End = tt.time()
        print(End-Start, 'seconds later')
        Dataset[t] = Dataset[kfloat]
        Dataset2[t] = Dataset[t]
        Counter2 = Counter2 + 1
    except IndexError:
        continue
        
#Find specified number of winning parameter sets 
z1 = Dataset2.iloc[2] #risk and return metric of choice
w1 = np.percentile(z1, (100 - lenthreshold)) #controls amount in winners Dataset2
v1 = [] #this variable stores the Nth percentile of top performers
winners = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset2.columns[(Dataset2 == j).iloc[2]]    
      winners = pd.concat([winners,Dataset2[r]], axis = 1) #winners variable is the SuperPortfolio parameters

y = max(z1)
k = Dataset2.columns[(Dataset2 == y).iloc[2]] #this is the name of the pair
kfloat = str(k[0])
