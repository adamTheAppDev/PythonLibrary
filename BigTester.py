# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: Adam Reinhold Von Fisher - adamrvfisher@gmail.com 
linkedin.com/in/adamrvfisher - github.com/adamrvfisher/TechnicalAnalysisLibrary
"""

#This is a portfolio analysis tool
#

#Load your modules
import numpy as np
import random as rand
import pandas as pd
import time as tt
from DatabaseAgeScanner import DatabaseAgeScanner
from DatabaseGrabber import DatabaseGrabber
#from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
#from SMAStrategyReturnStream import SMAStrategyReturnStream
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

#Make all pairs in final list by using the ListPairs function.

#MajorList = ListPairs(tickers)

#choose number of asset pairs in final equal weighted portfolio

listlen = len(tickers)
desiredlen = 10
lenthreshold = abs(int(round((1 -(((desiredlen)/listlen) - .0000001) * 100))))

Portfolio = pd.DataFrame()
#Here we go

#Brute Force Optimization
for t in tickers: #Every pair in pairlist
    try:
        #preliminary set up and 
        Ticker1 = t
        Dataset = pd.DataFrame()
        Asset1 = DatabaseGrabber(Ticker1)
    #get log returns
        Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
        Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

    #Match lengths
    
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
            
            Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp) #cumulative returns
            drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax()) #Max Drawdown calculation
            MaxDD = max(drawdown) 
#            if MaxDD > float(.5): 
#                continue
            
            dailyreturn = Asset1['Pass'].mean()
#            if dailyreturn < .0003:
#                continue
           
            #statistics
            dailyvol = Asset1['Pass'].std()
            sharpe =(dailyreturn/dailyvol)
            MaxDD = max(drawdown)
#            print(Counter)

            #save parameters for further analysis
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
    #find optimal parameters from pair
        z1 = Dataset.iloc[2] #large row of specific statistic
        w1 = np.percentile(z1, 80) #nth percentile of specific statistic
        v1 = [] #this variable stores the Nth percentile of top performers
        DS1W = pd.DataFrame() #this variable stores top parameters for specific dataset

        #populate v1 to make DS1W
        for h in z1:
            if h > w1:
              v1.append(h)

        #populate DS1W with parameters
        for j in v1:
              r = Dataset.columns[(Dataset == j).iloc[2]]    
              DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
        
        #find 'optimal' parameters for model and pass to Dataset2
        y = max(z1)
        k = Dataset.columns[(Dataset == y).iloc[2]] #this is the column number
        kfloat = float(k[0])
        End = tt.time()
#        print(End-Start, 'seconds later')
        Dataset[t] = Dataset[kfloat]
        Dataset2[t] = Dataset[t]
#        Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
        Counter2 = Counter2 + 1
#    print(Dataset[TAG])
    except IndexError:
        continue
#Portfolio2 = pd.DataFrame()
##find specified number of winning parameter sets 
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

#print(Dataset2[kfloat])
#num = kfloat.find('/')
#num2 = num + 1

#find length of shortest time series to trim the final portfolio
#shortest = min(winners.iloc[12])
#
##set up final portfolio
#SuperPortfolio = pd.DataFrame()
#
##use winners parameters to get returns streams for final portfolio 
#for jj in winners.columns:
#    SuperPortfolio[jj] = SMAStrategyReturnStream(winners[jj], shortest)
#
##number of positions to distribute equal weights to
#numpositions = len(SuperPortfolio.columns)
#equalweight = 1/numpositions
#AdjustedPortfolio = pd.DataFrame()
#
##Multiply weights to returns and add for final return stream 
#for jjj in SuperPortfolio.columns:
#    AdjustedPortfolio[jjj] = SuperPortfolio[jjj] * equalweight
#
#FinalReturnStream = pd.Series()
#
##Sum it all up
#FinalReturnStream = AdjustedPortfolio.sum(axis = 1)
#FinalReturnStream.cumsum().apply(np.exp).plot()
#FinalReturnStream[-1000:].cumsum().apply(np.exp).plot()
#
##Statistics
#PortfolioMultiplier = FinalReturnStream.cumsum().apply(np.exp)
#PortfolioDrawdown =  1 - PortfolioMultiplier.div(PortfolioMultiplier.cummax())
#PortfolioMaxDrawdown = max(PortfolioDrawdown) 
#Portfoliodailyreturn = FinalReturnStream.mean()
#Portfoliodailyvol = FinalReturnStream.std()
