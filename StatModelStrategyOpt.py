# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy model with a brute force optimizer + z score based signal

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

#Assign ticker
Ticker1 = 'UVXY'

#Read in // request data
Asset1 = pd.read_csv('UVXYnew.csv')
#Asset1 = YahooGrabber(Ticker1)

#Time series trimmer
Asset1 = Asset1[:-252]
#Number of iterations
iterations = range(0, 2000)

#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a = rand.randint(2,30)
    b = 3 - rand.random()*6
    c = rand.randint(2,30)
    #Variable assignment
    Rollwindow = a
    Zscorethreshold = b
    hold = c
    #Iterable for holding period
    ranger = range(0, hold)
    
    #Calculate log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset1['LogRet+1'] = Asset1['LogRet'] + 1
    
    #Summary statistics
    meanreturn = Asset1['LogRet'].mean()
    stdreturn = Asset1['LogRet'].std()
    #Calculate z-score
    Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
    Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
    #Summary statistics
    rollmeanreturn = Asset1['RollingRet'].mean()
    rollstdreturn = Asset1['RollingRet'].std()
    #Calculate rolling z-score
    Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn
    #Directional methodology
    Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                    -1, 0)
    #Asset1['Regime'] = np.where(Asset1['RollingZscore'] < (-Zscorethreshold * rollstdreturn),
                                    #1, 0)
    #Forward fill for hold period    
    for r in ranger:
        Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
        #Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == 1, 1, Asset1['Regime'])
    
    #Zeros
    Asset1['OriginalTrade'] = 0
    #Initial signal in stream of -1s
    Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1
    #Apply position to returns
    Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet']# * Asset1['Position']
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown stat
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > .6:
        continue

    #Performance metrics    
    dailyreturn = Asset1['Strategy'].mean()
    dailyvol = Asset1['Strategy'].std()
    #Constraint
    #if dailyvol == 0: 
        #continue
    #Performance metric    
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)
    #Save params and metrics to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
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
z1 = Dataset.iloc[4]
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
      r = Dataset.columns[(Dataset == j).iloc[4]]    
      #Add to list
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)

    #Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[4]]
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])

#Read in params
#Variable assignment
Rollwindow = int(Dataset[kfloat][0])
Zscorethreshold = Dataset[kfloat][1]
hold = int(Dataset[kfloat][3])
#Iterable for holding period
ranger = range(0, hold)

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['LogRet+1'] = Asset1['LogRet'] + 1

#Summary statistics
meanreturn = Asset1['LogRet'].mean()
stdreturn = Asset1['LogRet'].std()
#Calculate z-score
Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
#Summary statistics
rollmeanreturn = Asset1['RollingRet'].mean()
rollstdreturn = Asset1['RollingRet'].std()
#Calculate rolling z-score
Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn

#Directional methodology
Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                -1, 0)
#Asset1['Regime'] = np.where(Asset1['RollingZscore'] < (-Zscorethreshold * rollstdreturn),
#                                 1, 0)
#Forward fill for hold period
for r in ranger:
    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
#    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == 1, 1, Asset1['Regime'])
#Zeros
Asset1['OriginalTrade'] = 0
#Initial signal in stream of -1s
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1
#Apply position to returns

Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet'] #* Asset1['Position']
#Returns on $1
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#Incorrectly calculated drawdown stat
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
MaxDD = max(drawdown)

#Performance metrics
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
#Display results
print(MaxDD)    
#Graphical display
Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
