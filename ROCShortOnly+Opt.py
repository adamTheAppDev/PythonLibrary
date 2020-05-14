# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer; short only - volatility ETF

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
import random as rand
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
 
#Start timer
start = t.time()
#Iteration tracking
Counter = 0
#Empty structures
tempdf = pd.DataFrame()
edgelist = []
Empty = []
Dataset = pd.DataFrame()

#Issue selection
ticker = 'UVXY'

#Request data
Asset = YahooGrabber(ticker)

#Iterable
iterations = range(0,1000) 

#Time series trimmer
Asset = Asset[:]

#Represent index as column in Asset the DataFrame
Asset['Index'] = Asset.index
#Alternative range based index starting from 1, not 0
Asset['RangeIndex'] = range(1, len(Asset.index) + 1)

#Format for mpl - graphics
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)

#Format Dataframe to feed candlestick_ohlc() - graphics
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()

#Calculate log returns
Asset['LogRet'] = np.log(Asset['Adj Close']/Asset['Adj Close'].shift(1)) 
Asset['LogRet'] = Asset['LogRet'].fillna(0)

#For number of iterations
for n in iterations:
    #Generate random params
    ROC = -.000001 + (rand.random() * 2)
    ROCWindow = rand.randint(10,50)
    HoldPeriod = rand.randint(20,150)
    #ROC calculation
    Asset['RateOfChange'] = (Asset['High'] - Asset['Adj Close'].shift(ROCWindow)
                                  ) / Asset['Adj Close'].shift(ROCWindow)
    #Directional methodology
    Asset['Regime'] =  np.where(Asset['RateOfChange'] >  ROC, -1, np.nan)
    Asset['Regime'] = Asset['Regime'].ffill(limit = HoldPeriod)
    #Apply position to returns
    Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
    Asset['Strategy'] = Asset['Strategy'].fillna(0)
    #Returns on $1
    Asset['Multiplier'] = Asset['Strategy'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown statistic
    drawdown =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
    Asset['drawdown'] =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
    MaxDD = max(drawdown)
   
    #Performance metrics
    dailyreturn = Asset['Strategy'].mean()
    dailyvol = Asset['Strategy'].std()
    #Constraint
    if dailyvol == 0:
        continue
    #Performance metric  
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    Counter = Counter + 1
    #Constraints
    #if MaxDD > .59:
        #continue
    #if dailyreturn < 0.0085:
        #continue
    #Performance metrics
    Sharpe = dailyreturn/dailyvol
    SharpeOverMaxDD = Sharpe/MaxDD
    #Add params and metrics to list
    Empty.append(ROC)
    Empty.append(ROCWindow)
    Empty.append(HoldPeriod)
    Empty.append(dailyreturn)
    Empty.append(dailyvol)
    Empty.append(Sharpe)
    Empty.append(SharpeOverMaxDD)
    Empty.append(MaxDD)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[n] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
    #Iteration tracking
    print(Counter)

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
#print(End-Start, 'seconds later')
#Display results
print(Dataset[k])

#Read in metrics
ROC = Dataset[kfloat][0]
ROCWindow = Dataset[kfloat][1]
HoldPeriod = Dataset[kfloat][2]

#ROC calculation
Asset['RateOfChange'] = (Asset['Adj Close'] - Asset['Adj Close'].shift(ROCWindow)
                              ) / Asset['Adj Close'].shift(ROCWindow)

#Directional methodology
Asset['Regime'] =  np.where(Asset['RateOfChange'] >  ROC, -1, np.nan)
#Forward fill position
Asset['Regime'] = Asset['Regime'].ffill(limit = HoldPeriod)
#Apply returns to position
Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
Asset['Strategy'] = Asset['Strategy'].fillna(0)
#Graphical display
Asset[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
