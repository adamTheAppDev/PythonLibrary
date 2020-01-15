# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: Adam Reinhold Von Fisher
linkedin.com/in/adamrvfisher
"""

#This is a massive two asset portfolio tester with a brute force optimizer
#Takes all pair combos, tests, and sorts. 

#Load your modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
#from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
from SMAStrategyReturnStream import SMAStrategyReturnStream

#Preliminary assignment

Empty = [] #list
Start = t.time() #timer
Counter = 0
Counter2 = 0
iterations = range(0, 500) #Loop size
Dataset2 = pd.DataFrame() #Extra DataFrame

#Input

tickers = ('AA', 'AAME', 'AAN', 'AAON', 'AAPL', 'AB', 'ABAX', 'ABC', 'ABCB', 'ABEO', 'ABEV')

#Make all pairs in final list by using the ListPairs function.

MajorList = ListPairs(tickers)

#choose number of asset pairs in final equal weighted portfolio

listlen = len(MajorList)
desiredlen = 2
lenthreshold = abs(int(round((1 -(((desiredlen+1)/listlen) - .0000001) * 100))))

#Here we go

#Brute Force Optimization
for m in MajorList: #Every pair in pairlist
    try:
        #preliminary set up and 
        Dataset = pd.DataFrame()
        Ticker1 = m[0]
        Ticker2 = m[1]
        TAG = m[0] + '/' + m[1]
        Dataset = pd.DataFrame()
        Portfolio = pd.DataFrame()
    #pull online data, change to local for testing
    #    Asset1 = YahooGrabber(Ticker1)
    #    Asset2 = YahooGrabber(Ticker2)  
        Asset1 = DatabaseGrabber(Ticker1)
        Asset2 = DatabaseGrabber(Ticker2)  
    #get log returns
        Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
        Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
        Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
        Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
    #Match lengths
        trim = abs(len(Asset1) - len(Asset2))
        if len(Asset1) == len(Asset2):
            pass
        else:
            if len(Asset1) > len(Asset2):
                Asset1 = Asset1[trim:]
            else:
                Asset2 = Asset2[trim:]
    
    #Run random variables through model and acquire parameters
    
        for i in iterations:
            Counter = Counter + 1
            aa = rand.random() * 2 #uniformly distributed random number 0 to 2
            a = aa - 1          #a > 1 indicating long position in a
            bb = rand.random()
            if bb >= .5:
                bb = 1
            else:
                bb = -1
            b = bb * (1 - abs(a))
    
    #you can change c and d to 0 by default if you want to just go flat
    
            cc = rand.random() * 2 #uniformly distributed random number 0 to 2
            c = cc - 1          #cc > 1 indicating long position in c
            dd = rand.random() * 2
            if dd >= 1:
                edd = 1
            else:
                edd = -1
            d = (dd - 1)
            if abs(c) + abs(d) > 1:
                continue
            e = rand.randint(3,25)
            f = rand.randint(3,25)
    
            #SMA lookback window 
    
            window = int(e)
            window2 = int(f)

            #SMA calculation            
            Asset1['SMA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
            Asset2['SMA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()        
            
            #fixed size position for a and b, alternative fixed positions of c and d 
            
            Asset1['Position'] = a
            Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['SMA'].shift(1),
                                            c,a)                                    
            Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position']) #position size * returns
    
            Asset2['Position'] = b
            Asset2['Position'] = np.where(Asset2['Adj Close'].shift(1) > Asset2['SMA'].shift(1),
                                            d,b)
            Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position']) #position size * returns

            #Pass individual adjusted return streams to dual asset portfolio
            Portfolio['Asset1Pass'] = (Asset1['Pass']) 
            Portfolio['Asset2Pass'] = (Asset2['Pass']) 

            #Add to make dual asset portfolio
            Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 

            if Portfolio['ReturnStream'].std() == 0:    
                continue
            
            Portfolio['Multiplier'] = Portfolio['ReturnStream'].cumsum().apply(np.exp) #cumulative returns
            drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax()) #Max Drawdown calculation
            MaxDD = max(drawdown) 
            if MaxDD > float(.5): 
                continue
            
            dailyreturn = Portfolio['ReturnStream'].mean()
            if dailyreturn < .0003:
                continue
           
            #statistics
            dailyvol = Portfolio['ReturnStream'].std()
            sharpe =(dailyreturn/dailyvol)
            MaxDD = max(drawdown)
            print(Counter)

            #save parameters for further analysis
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
            Empty.append(m[0])
            Empty.append(m[1])
            Empty.append(len(Portfolio))
            
            Emptyseries = pd.Series(Empty)
            Dataset[0] = Emptyseries.values
            Dataset[i] = Emptyseries.values
            Empty[:] = [] 
    #find optimal parameters from pair
        z1 = Dataset.iloc[7] #large row of specific statistic
        w1 = np.percentile(z1, 80) #nth percentile of specific statistic
        v1 = [] #this variable stores the Nth percentile of top performers
        DS1W = pd.DataFrame() #this variable stores top parameters for specific dataset

        #populate v1 to make DS1W
        for h in z1:
            if h > w1:
              v1.append(h)

        #populate DS1W with parameters
        for j in v1:
              r = Dataset.columns[(Dataset == j).iloc[7]]    
              DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
        
        #find 'optimal' parameters for model and pass to Dataset2
        y = max(z1)
        k = Dataset.columns[(Dataset == y).iloc[7]] #this is the column number
        kfloat = float(k[0])
        End = t.time()
        print(End-Start, 'seconds later')
        Dataset[TAG] = Dataset[kfloat]
        Dataset2[TAG] = Dataset[TAG]
        Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
        Counter2 = Counter2 + 1
#    print(Dataset[TAG])
    except IndexError:
        continue
Portfolio2 = pd.DataFrame()
#find specified number of winning parameter sets 
z1 = Dataset2.iloc[7] #risk and return metric of choice
w1 = np.percentile(z1, (100 - lenthreshold)) #controls amount in winners DataFrame
v1 = [] #this variable stores the Nth percentile of top performers
winners = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset2.columns[(Dataset2 == j).iloc[7]]    
      winners = pd.concat([winners,Dataset2[r]], axis = 1) #winners variable is the SuperPortfolio parameters

#y = max(z1)
#k = Dataset2.columns[(Dataset2 == y).iloc[7]] #this is the name of the pair
#kfloat = str(k[0])

#print(Dataset[TAG])
#num = kfloat.find('/')
#num2 = num + 1

#find length of shortest time series to trim the final portfolio
shortest = min(winners.iloc[12])

#set up final portfolio
SuperPortfolio = pd.DataFrame()

#use winners parameters to get returns streams for final portfolio 
for jj in winners.columns:
    SuperPortfolio[jj] = SMAStrategyReturnStream(winners[jj], shortest)

#number of positions to distribute equal weights to
numpositions = len(SuperPortfolio.columns)
equalweight = 1/numpositions
AdjustedPortfolio = pd.DataFrame()

#Multiply weights to returns and add for final return stream 
for jjj in SuperPortfolio.columns:
    AdjustedPortfolio[jjj] = SuperPortfolio[jjj] * equalweight

FinalReturnStream = pd.Series()

#Sum it all up
FinalReturnStream = AdjustedPortfolio.sum(axis = 1)
FinalReturnStream.cumsum().apply(np.exp).plot()
FinalReturnStream[-1000:].cumsum().apply(np.exp).plot()

#Statistics
PortfolioMultiplier = FinalReturnStream.cumsum().apply(np.exp)
PortfolioDrawdown =  1 - PortfolioMultiplier.div(PortfolioMultiplier.cummax())
PortfolioMaxDrawdown = max(PortfolioDrawdown) 
Portfoliodailyreturn = FinalReturnStream.mean()
Portfoliodailyvol = FinalReturnStream.std()
