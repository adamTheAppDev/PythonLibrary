# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017
"""

#This is a portfolio strategy tool with brute force optimizer
#Takes 2 assets to examine and a third for signal generation

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Input

#Ticker1 = 'UVXY'
#Ticker2 = '^VIX'
#
##Contango Signal will consist of VIX/VXV 
#Ticker3 = '^VXV'

#Grab data
#Asset1 = YahooGrabber(Ticker1)
#Asset2 = YahooGrabber(Ticker2)
#
##Remote Signal
#Asset3 = YahooGrabber(Ticker3)

#Grab data
Asset1 = pd.read_pickle('TastyUVXY')

Asset2 = pd.read_pickle('TastyVIX')

Asset3 = pd.read_pickle('TastyVXV')

#Match lengths
#Trimmer - trim main dataframes to equal length
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Trim 
Asset3 = Asset3[-len(Asset2):]



#Prepare log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Prepare the remote signal, 1 month / 3 month  

Asset3['Contango'] = (Asset2['Close']/Asset3['Close'])

##Retrim Assets
#Asset1 = Asset1[window:]
#Asset2 = Asset2[window:]                             
#Asset3 = Asset3[window:]

#Brute Force Optimization - 2000 iterations on a 2012 Macbook takes about 14 seconds
iterations = range(0, 2000)

for i in iterations:
    #count the iterations....
    Counter = Counter + 1
    #represents position in Asset1 = a, Asset2 = b
    a = rand.random()
    b = 1 - a
    #represents position in Asset1 = c, Asset2 = d, given signal e is 'true'
    c = rand.random()
    d = 1 - c
    #e will represent a threshold for VIX/VXV where the positions a and b will
    #be switched to c and d ----- 'opportunistic short for UVXY' 
    #the strategy logic can be improved upon but it is not relevant for my questioning
    e = 1.5 - (rand.random()*.5)
    
    #a is default position for UVXY
    Asset1['Position'] = a
    #when VIX/VXV rises above threshold e, use c instead of a for position in Asset1
    Asset1['Position'] = np.where(Asset3['Contango'].shift(1) > e,
                                    c,a)   
    #we will 'pass' log returns multiplied by position size to the portfolio dataframe
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #b is default position for VIX    
    Asset2['Position'] = b
    #when VIX/VXV rises above threshold e, use d instead of b for position in Asset2
    Asset2['Position'] = np.where(Asset3['Contango'].shift(1) > e,
                                    d,b)
    #we will 'pass' log returns multiplied by position size to the portfolio dataframe           
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position on Asset1 to portfolio
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)

    #Add respective 'pass' to get total return 
    Portfolio['TotalRet'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass'])
    
    #avoid dividing by 0 for errors/shorten optimization time
    if Portfolio['TotalRet'].std() == 0:    
        continue
    
    
    Portfolio['Multiplier'] = Portfolio['TotalRet'].cumsum().apply(np.exp)
    
    #find drawdowns
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    
    #eliminate unattractive drawrdown iterations/shorten optimization
    if MaxDD > float(.3): 
        continue
    #eliminate unattractive return iterations/shorten optimization 
    dailyreturn = Portfolio['TotalRet'].mean()
    if dailyreturn < .002:
        continue

    #you get the idea
    dailyvol = Portfolio['TotalRet'].std()
    
    #well, no risk free rate of return..
    sharpe =(dailyreturn/dailyvol)
    
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    print(Counter)
    
    #This part stores 'successful' iteration parameters in a list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    
    #List to vertical series
    Emptyseries = pd.Series(Empty)
    #Concatenate Vertical Series - Horizontally to Dataframe
    Dataset[i] = Emptyseries.values
    #Clear out the list for the next iteration! Rinse and repeat.
    Empty[:] = []






#Now we are outside the loop and want to grab an attractive iteration
#z1 stores a horizonal series of sharpe/MaxDD statistics    
z1 = Dataset.iloc[6]
#w1 is the threshold value for top 80 percentile of highest 'sharpe' to maxDD 
w1 = np.percentile(z1, 80)
v1 = [] #this list stores the 80 to 100 percentile of highest 'sharpe' to maxDD from the first for loop
DS1W = pd.DataFrame() #this variable stores your Vertical Series with parameters concatenated horizontally
for h in z1: #for all 'sharpe' to maxDD parameters
    if h > w1: #if you are above 80% threshold
      v1.append(h) #you are part of v1
for j in v1: #for all parameters in v1
      r = Dataset.columns[(Dataset == j).iloc[6]] #grab the entire Vertical series of parameters associated with specific element of z1
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1) # and concatenate that to an empty dataframe, just like the 'Dataset' variable
y = max(z1) #find the winning-est parameter set based on max(sharpe/maxDD) from entire simulation
k = Dataset.columns[(Dataset == y).iloc[6]] #this is the column number from Dataset
kfloat = float(k[0]) #reference column number as float
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k]) #Attractive parameter set

#Now lets run the model and see what the attractive parameter set looks like.
  
Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Position'] = np.where(Asset3['Contango'].shift(1) > Dataset[kfloat][4],
                                    Dataset[kfloat][2],Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])

Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Position'] = np.where(Asset3['Contango'].shift(1) > Dataset[kfloat][4],
            Dataset[kfloat][3],Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)

Portfolio['TotalRet'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
Portfolio['TotalRet'][:].cumsum().apply(np.exp).plot(grid=True, figsize=(8,5))
dailyreturn = Portfolio['TotalRet'].mean()
dailyvol = Portfolio['TotalRet'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio['Multiplier'] = Portfolio['TotalRet'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())

print('Max drawdown is about ' + str(round((max(drawdown2)*100),2)) +'%')
