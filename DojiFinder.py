# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Doji candle finded
#This is a techincal analysis tool and strategy tester

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import random as rand
import pandas as pd

#Input ticker
Ticker = 'MS'
#Variable assignment
iterations = range(0, 2000)
Counter = 0
Empty = []
Dataset = pd.DataFrame()
#Data request
Asset1 = YahooGrabber(Ticker)
#Trimmer
#Asset1 = Asset1[-2000:]
#Random number for trailing position - can use .ffill(limit = n) instead
trail = rand.randint(3,40)
trailrange = range(1,trail)
#For number of iterations in brute force optimization
for i in iterations:
    #SMA window assignment
    window = rand.randint(3,100)
    #Magnitude AKA doji sensitivity
    mag = rand.random()/500
    #Calculate log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    #SMA calculation
    Asset1['SMA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
    #Price to SMA ratio
    Asset1['Trend'] = (Asset1['Adj Close']/Asset1['SMA']) - 1
    #Open to close ratio
    Asset1['DojiFactor'] = Asset1['Open']/Asset1['Adj Close'] 
    #Absolute value of open to close return
    Asset1['MAGN'] = abs(1 - Asset1['DojiFactor'])
    #Is Doji -- does return hit sensitivity threshold
    Asset1['Doji?'] = np.where(Asset1['MAGN'] < mag, 1, 0)
    #Directional methodology
    Asset1['Sign'] = np.where(Asset1['Trend'].shift(1) < 0, 1, -1)
    #If is doji, take directional assumption
    Asset1['Position'] = (Asset1['Doji?'] * Asset1['Sign'])  
    #Should be using .ffill(limit = n)
    Asset1['AddlPosition'] = 0
    #For number of days to .ffill()
    for t in trailrange:
        Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == 1, 1, Asset1['AddlPosition'])
        Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == -1, -1, Asset1['AddlPosition'])
    #Total position adds first day to amount of days forward filled
    Asset1['TotalPosition'] = Asset1['Position'] + Asset1['AddlPosition']
    Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == -2, -1, Asset1['AddlPosition'])
    Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == 2, 1, Asset1['AddlPosition'])
    #Returns from strategy
    Asset1['Pass'] = Asset1['TotalPosition'] * Asset1['LogRet'] 
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
    #Iteration tracking
    Counter = Counter + 1
    print(Counter)
    #Spurious drawdown metric
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    #Performance metric
    dailyreturn = Asset1['Pass'].mean()
    #Constraint
    if dailyreturn < 0:
        continue
    #Performance metric    
    dailyvol = Asset1['Pass'].std()
    #Constraint
    if Asset1['Pass'].std() == 0:    
        continue
    #Performance metric
    sharpe =(dailyreturn/dailyvol)
    #Spurious max drawdown stat
    MaxDD = max(drawdown)

    #Save params and performance metrics to temp list
    Empty.append(window)
    Empty.append(mag)
    Empty.append(trail)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    #Clear list for next iteration
    Empty[:] = [] 
    
#Find optimal parameters from simulation
z1 = Dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #This variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #This variable stores your params for specific dataset
#For all return metrics
for l in z1:
    #If above threshold
    if l > w1:
      #Add to list
      v1.append(l)
#For all params above threshold
for j in v1:
      #Find column number
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      #Add to DataFrame
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Optimal param set
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])

#Testing optimal param set in model
#window = int(Dataset[kfloat][0])
#mag = Dataset[kfloat][1]
#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
#SMA calculation
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=int(Dataset[kfloat][0]), center=False).mean()
#Price / SMA - 1
Asset1['Trend'] = (Asset1['Adj Close']/Asset1['SMA']) - 1
#Candle Doji-ness
Asset1['DojiFactor'] = Asset1['Open']/Asset1['Adj Close'] 
#Is doji? -- does candle fit doji threshold
Asset1['MAGN'] = abs(1 - Asset1['DojiFactor'])
Asset1['Doji?'] = np.where(Asset1['MAGN'] < Dataset[kfloat][1], 1, 0)
#Directional assumption
Asset1['Sign'] = np.where(Asset1['Trend'].shift(1) < 0, 1, -1)
Asset1['Position'] = (Asset1['Doji?'] * Asset1['Sign']) 
#For use in .ffill()
Asset1['AddlPosition'] = 0
#How many days to .ffill()
trail = int(Dataset[kfloat][2])
trailrange = range(1,trail)
#Should use .ffill(limit = n) here not for loop 
for t in trailrange:
    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == 1, 1, Asset1['AddlPosition'])
    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == -1, -1, Asset1['AddlPosition'])

#Aggregating directional assumptions
Asset1['TotalPosition'] = Asset1['Position'] + Asset1['AddlPosition'] 
Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == -2, -1, Asset1['AddlPosition'])
Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == 2, 1, Asset1['AddlPosition'])
#Strategy returns
Asset1['Pass'] = Asset1['TotalPosition'] * Asset1['LogRet'] 
#Returns on $1
Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
#Spurious drawdown calculation
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
#Performance metrics
dailyreturn = Asset1['Pass'].mean()
dailyvol = Asset1['Pass'].std()
sharpe =(dailyreturn/dailyvol)
MaxDD = max(drawdown)
#Display
print(MaxDD)
Asset1['Multiplier'].plot()
#Optimal param set
print(Dataset[kfloat])
