# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""


#This is a massive two asset portfolio tester with a brute force optimizer
#Takes all pair combos, tests, and sorts. 

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
#from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
from SMAStrategyReturnStream import SMAStrategyReturnStream

#Empty data structures
Empty = [] #listr
Counter = 0
Counter2 = 0
Dataset2 = pd.DataFrame() #Extra DataFrame

#Iterable
iterations = range(0, 500) #Loop size

#Start timer
Start = t.time() 

#Assign tickers
tickers = ('AA', 'AAME', 'AAN', 'AAON', 'AAPL', 'AB', 'ABAX', 'ABC', 'ABCB', 'ABEO', 'ABEV')

#Make all pairs in final list
MajorList = ListPairs(tickers)

#Choose number of asset pairs in final equal weighted portfolio
listlen = len(MajorList)
desiredlen = 2
lenthreshold = abs(int(round((1 -(((desiredlen+1)/listlen) - .0000001) * 100))))

#For all pairs in Brute Force Optimization
for m in MajorList: 
    try:
        #Read in tickers
        Ticker1 = m[0]
        Ticker2 = m[1]
        TAG = m[0] + '/' + m[1]
        #Empty data structures
        Dataset = pd.DataFrame()
        Portfolio = pd.DataFrame()
        
        #Request data  
        Asset1 = DatabaseGrabber(Ticker1)
        Asset2 = DatabaseGrabber(Ticker2)  
        
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
            if bb >= .5:
                bb = 1
            else:
                bb = -1
            b = bb * (1 - abs(a))
            #Change c and d to 0 by default if you want to just go flat
            #Generate random params
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
              
            #Assign params
            window = int(e)
            window2 = int(f)

            #SMA calculation            
            Asset1['SMA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
            Asset2['SMA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()        
           
            #Position sizing
            Asset1['Position'] = a
            #Alternative position sizing
            Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['SMA'].shift(1),
                                            c,a)                                    
            #Apply position to returns
            Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position']) 
            #Position sizing
            Asset2['Position'] = b
            #Alternative position sizing
            Asset2['Position'] = np.where(Asset2['Adj Close'].shift(1) > Asset2['SMA'].shift(1),
                                            d,b)
            #Apply position to returns
            Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position']) #position size * returns

            #Pass individual return streams to portfolio
            Portfolio['Asset1Pass'] = (Asset1['Pass']) 
            Portfolio['Asset2Pass'] = (Asset2['Pass']) 

            #Portfolio returns
            Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
            #Constraint
            if Portfolio['ReturnStream'].std() == 0:    
                continue
           
            #Returns on $1
            Portfolio['Multiplier'] = Portfolio['ReturnStream'].cumsum().apply(np.exp) #cumulative returns
            #Incorrectly calculated max drawdown
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
            #Incorrectly calculated max drawdown
            MaxDD = max(drawdown)
            #Iteration
            print(Counter)

            #Save parameters and metrics to list
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
            #List to series
            Emptyseries = pd.Series(Empty)
            #Series to dataframe
            Dataset[i] = Emptyseries.values
            #Clear list
            Empty[:] = [] 
        #Metric of choice
        z1 = Dataset.iloc[7] 
        #Threshold
        w1 = np.percentile(z1, 80)
        v1 = [] #this variable stores the Nth percentile of top params
        DS1W = pd.DataFrame() #this variable stores top parameters for specific dataset

        #For all metrics
        for h in z1:
            #If greater than threshold 
            if h > w1:
              #Add to list  
              v1.append(h)

        #For top metrics
        for j in v1:
              #Get column ID of metric
              r = Dataset.columns[(Dataset == j).iloc[7]]    
              #Add to list
              DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
        
        #Top metric
        y = max(z1)
        #Column ID of top metric
        k = Dataset.columns[(Dataset == y).iloc[7]] 
        #Column ID of top metric - float
        kfloat = float(k[0])
        #End timer
        End = t.time()
        #Timer stats
        print(End-Start, 'seconds later')
        #Assign params
        Dataset[TAG] = Dataset[kfloat]
        Dataset2[TAG] = Dataset[TAG]
        #Rename dataframe columns
        Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
        #Iteration tracking
        Counter2 = Counter2 + 1
    #print(Dataset[TAG])
    except IndexError:
        continue
#Create dataframe        
Portfolio2 = pd.DataFrame()
#Metric of choice
z1 = Dataset2.iloc[7] 
#Threshold
w1 = np.percentile(z1, (100 - lenthreshold))
v1 = [] #this variable stores the Nth percentile of top params
winners = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list  
      v1.append(h)
#For top metrics        
for j in v1:
      #Get column ID of metric
      r = Dataset2.columns[(Dataset2 == j).iloc[7]]    
      #Add to dataframe
      winners = pd.concat([winners,Dataset2[r]], axis = 1)

#Find length of shortest time series to trim the final portfolio
shortest = min(winners.iloc[12])

#Set up final portfolio
SuperPortfolio = pd.DataFrame()

#Use winners parameters to get returns streams for final portfolio 
for jj in winners.columns:
    SuperPortfolio[jj] = SMAStrategyReturnStream(winners[jj], shortest)

#Number of positions to distribute equal weights to
numpositions = len(SuperPortfolio.columns)
equalweight = 1/numpositions
AdjustedPortfolio = pd.DataFrame()

#Multiply weights to returns and add for final return stream 
for jjj in SuperPortfolio.columns:
    AdjustedPortfolio[jjj] = SuperPortfolio[jjj] * equalweight

#Empty series
FinalReturnStream = pd.Series()

#Sum it all up
FinalReturnStream = AdjustedPortfolio.sum(axis = 1)
FinalReturnStream.cumsum().apply(np.exp).plot()
FinalReturnStream[-1000:].cumsum().apply(np.exp).plot()

#Returns on $1
PortfolioMultiplier = FinalReturnStream.cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
PortfolioDrawdown =  1 - PortfolioMultiplier.div(PortfolioMultiplier.cummax())
PortfolioMaxDrawdown = max(PortfolioDrawdown) 
#Performance metrics
Portfoliodailyreturn = FinalReturnStream.mean()
Portfoliodailyvol = FinalReturnStream.std()
