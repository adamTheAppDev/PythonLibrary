# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from pandas import read_csv
#Empty data structures
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Counter = 0

#Start timer
Start = t.time()

#Assign tickers
#Ticker1 = 'UVXY'
#Ticker2 = '^VIX'
#Ticker3 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)

#For CC futures csv
#Asset2 = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\VX1CC.csv', sep = ',')
#Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
#Asset2 = Asset2.set_index('Date')
#Asset2 = Asset2.reindex(index=Asset2.index[::-1])

#Out of Sample Selection
Asset1 = Asset1[:-252]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Number of iterations for Brute Force Optimization
iterations = range(0, 1000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a = 1
    c = rand.random()
    e = rand.randint(8,100)
    window = int(e)
    #Calculate simple moving average
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
    #Directional methodology
    Asset1['Regime'] = np.where(Asset1['MA'] < Asset1['Adj Close'], 1 , -1)                                 
    #Apply position to returns
    Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'].shift(1))
    #Constraint
    #if Asset1['Strategy'].std() == 0:    
        #continue
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.721): 
            continue
    #Performance metric
    dailyreturn = Asset1['Strategy'].mean()
    #Constraint
    #if dailyreturn < .003:
            #continue
    #Performance metrics
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    #Save params and metric to list    
    print(Counter)
    Empty.append(a)
    Empty.append(c)
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
      #Get column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      #Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[3]]
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top param set
print(Dataset[k])

#Read in params 
window = int((Dataset[kfloat][2]))
#Calculate simple moving average
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()   
#Directional methodology
Asset1['Regime'] = np.where(Asset1['MA'] < Asset1['Adj Close'], 1 , -1)
#Apply position to returns
Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'].shift(1))
#Graphical display
Asset1['Strategy'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()
sharpe = (dailyreturn / dailyvol)
#Returns on $1
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
#Display results
print(max(drawdown))
