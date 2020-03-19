# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset strategy tester with a brute force optimization and 
#a reallocation based on drawdown, may not be suitable for real life
#Potentially a lot of curve fitting going on here. 

#Dynamic Weighting

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabberII import YahooGrabberII

#Variable assignment
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Ticker Assignment - input
Ticker1 = 'UVXY' #Short Position
Ticker2 = 'VXX' #Long Position

#Grab local data
Asset1 = DatabaseGrabber(Ticker1)
Asset2 = DatabaseGrabber(Ticker2)


#Request data
#Asset1 = YahooGrabberII(Ticker1)
#Asset2 = YahooGrabberII(Ticker2)

#Trim time serioes to match lengths
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#In/out sample trimmer
#Asset1 = Asset1[-100:]
#Asset2 = Asset2[-100:]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Brute Force Optimization
#Number of loops for optimization
iterations = range(0, 200)

#For each iteration
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Random variable generation and assignment
    a = rand.random()
    b = 1 - a
    c = 1.5 - (rand.random() * 3 )
    d = b - rand.random()
    e = 4 - (rand.random() * 8 )
    f = b - rand.random()
    
    #Constraint
    if abs(c) > abs(e):
        continue
    #Position sizing
    Asset1['Position'] = a
    #Apply returns to position size
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    #Apply returns to position size
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Variable assignment of position size
    Asset1Position = a
    Asset2Position = b
    #Pass position sizes to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) 
    Portfolio['Asset2Pass'] = (Asset2['Pass'])
    #Portfolio returns
    Portfolio['LongShort'] = (Portfolio['Asset1Pass'] * -1) + (Portfolio['Asset2Pass']) #Pass a short position
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

    #Performance statistics
    DailyReturn = Portfolio['LongShort'].mean()
    #Constraint
#    if DailyReturn < .0025:
#        continue
    #Performance statistics
    DailyVol = Portfolio['LongShort'].std()
    #Constraint
    if Portfolio['LongShort'].std() == 0:
        continue
    #Performance statistics
    Sharpe = (DailyReturn/DailyVol)
    #Incorrectly calculated drawdown metric - pls fix
    DrawDown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    Portfolio['DrawDown'] = DrawDown
    MaxDD = max(DrawDown)
    #Constraint
#    if MaxDD > .25:
#        continue
#    if MaxDD < .05:
#        continue
    #Incorrectly calculated drawdown metric - pls fix
    AvgDrawDown = Portfolio['DrawDown'].mean()
    StdDrawDown = Portfolio['DrawDown'].std()

    #New allocation weights during regime change - looks like it gets written over in next couple lines
    Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (+/-c*StdDrawDown), 
                   (c * StdDrawDown)), (Asset1Position + d), Asset1['Position']) #d
    #This will be subtracted from 1 to get Portfolio['Asset2NewPosition']
    Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #e (+/-e*StdDrawDown), 
                   (e * StdDrawDown)), (Asset1Position + f), Asset1['Position'])
    #Complement of position 1 to portfolio - all capital is allocated
    Portfolio['NewAsset2Position'] = 1 - Portfolio['NewAsset1Position'] #    np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (AvgDrawDown (+/-c*StdDrawDown)), 
#                    (c * StdDrawDown)), (Asset2Position + e), Asset2['Position']) #e
    #Passing new positions to portfolio
    Portfolio['Asset1NewPass'] = (Asset1['LogRet'] * Portfolio['NewAsset1Position'])                            
    Portfolio['Asset2NewPass'] = (Asset2['LogRet'] * Portfolio['NewAsset2Position'])
    #Apply position to return steam
    Portfolio['NewLongShort'] = (Portfolio['Asset1NewPass'] * -1) + (Portfolio['Asset2NewPass']) #Pass a short position
    #Returns on $1
    Portfolio['NewMultiplier'] = Portfolio['NewLongShort'].cumsum().apply(np.exp)

    #Performance statistics
    NewDailyReturn = Portfolio['NewLongShort'].mean()
    #Constraints
#    if NewDailyReturn < DailyReturn:
#        continue
#    if NewDailyReturn < .0025:
#        continue
    #Performance statistics
    NewDailyVol = Portfolio['NewLongShort'].std()
    #Constraints
#    if Portfolio['NewLongShort'].std() == 0:    
#        continue
    #Performance statistics
    NewSharpe =(NewDailyReturn/(NewDailyVol))
    #Incorrectly calculated drawdown statistic
    NewDrawDown =  1 - Portfolio['NewMultiplier'].div(Portfolio['NewMultiplier'].cummax())
    Portfolio['NewDrawDown'] = NewDrawDown
    NewMaxDD = max(NewDrawDown)
    #Constraints
#    if NewMaxDD > .25:
#        continue
#    if NewMaxDD < .12:
#        continue
    #Spurious, incorrect until fixes
    NewAvgDrawDown = Portfolio['NewDrawDown'].mean()
    NewStdDrawDown = Portfolio['NewDrawDown'].std()

#Graphical display
#Portfolio['NewLongShort'][:].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
    #Iteration tracking                             
    print(Counter) 
    #Save params/metrics to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)  
    Empty.append(f)  
    Empty.append(Sharpe)
    Empty.append(Sharpe/MaxDD)
    Empty.append(DailyReturn/MaxDD)
    Empty.append(MaxDD)
    Empty.append(NewSharpe)
    Empty.append(NewSharpe/NewMaxDD)
    Empty.append(NewDailyReturn/NewMaxDD)
    Empty.append(NewMaxDD)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Store series in dataset
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
#Find all entries of desired performance metric
z1 = Dataset.iloc[11]
#Find Nth percentile threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For metric in all desired metrics
for h in z1:
    #If metric above threshold
    if h > w1:
      #Add metric to list
      v1.append(h)
#For all metrics above threshold
for j in v1:
    #Get column number of specific metric
    r = Dataset.columns[(Dataset == j).iloc[11]]    
    #Add metric to parameter table
    DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top parameter    
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[11]] #this is the column number
#Param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])
                                 
#Testing based on top param set
#Position sizing
Asset1['Position'] = (Dataset[kfloat][0]) #a
#Apply position size to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = (Dataset[kfloat][1]) #b
#Apply position size to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Position size from top params
Asset1Position = Dataset[kfloat][0]#a
Asset2Position = Dataset[kfloat][1]#b
#Pass to portfolio
Portfolio['Asset1Pass'] = (Asset1['Pass']) 
Portfolio['Asset2Pass'] = (Asset2['Pass'])
#Combined returns 
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] * -1) + (Portfolio['Asset2Pass']) #Pass a short position
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Performance metric
DailyReturn = Portfolio['LongShort'].mean()
#Constraint
#    if dailyreturn < .0015:
#        continue
#Performance metric
DailyVol = Portfolio['LongShort'].std()
#Constraint
#   if Portfolio['LongShort'].std() == 0:    
#        continue
#Performance metric
Sharpe = (DailyReturn/DailyVol)
#Incorrectly calculated drawdown stat, pls fix
DrawDown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
Portfolio['DrawDown'] = DrawDown
MaxDD = max(DrawDown)
AvgDrawDown = Portfolio['DrawDown'].mean()
StdDrawDown = Portfolio['DrawDown'].std()

#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))

#Dynamic weighting from regime change
Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (+/-Dataset[kfloat][2]*StdDrawDown), 
                (Dataset[kfloat][2]*StdDrawDown)
                ), (Asset1Position + Dataset[kfloat][3]), Asset1['Position'])#d, Dataset[kfloat][3]
Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #e (+/-e*StdDrawDown), 
                (Dataset[kfloat][4]*StdDrawDown)
                ), (Asset1Position + Dataset[kfloat][5]), Asset1['Position'])#d, Dataset[kfloat][3]
Portfolio['NewAsset2Position'] = 1 - Portfolio['NewAsset1Position'] #np.where(Portfolio['DrawDown'] > (AvgDrawDown + #e (AvgDrawDown (+/-Dataset[kfloat][4]*StdDrawDown)), 
                #(Dataset[kfloat][4]*StdDrawDown)
                #), (Asset2Position + Dataset[kfloat][5]), Asset2['Position']) #Dataset[kfloat][5]

#Pass to portfolio
Portfolio['Asset1NewPass'] = (Asset1['LogRet'] * Portfolio['NewAsset1Position'])                            
Portfolio['Asset2NewPass'] = (Asset2['LogRet'] * Portfolio['NewAsset2Position'])
#Combine for return stream
Portfolio['NewLongShort'] = (Portfolio['Asset1NewPass'] * -1) + (Portfolio['Asset2NewPass']) #Pass a short position
Portfolio['NewMultiplier'] = Portfolio['NewLongShort'].cumsum().apply(np.exp)

#Performance metrics
NewDailyReturn = Portfolio['NewLongShort'].mean()
#Constraints
#    if dailyreturn < .0015:
#        continue
#Performance metrics
NewDailyVol = Portfolio['NewLongShort'].std()
#Constraints
#   if Portfolio['NewLongShort'].std() == 0:    
#        continue
#Performance metrics
NewSharpe =(NewDailyReturn/(NewDailyVol))
#Incorrectly calculated drawdown metric, pls fix
NewDrawDown =  1 - Portfolio['NewMultiplier'].div(Portfolio['NewMultiplier'].cummax())
Portfolio['NewDrawDown'] = NewDrawDown
NewMaxDD = max(NewDrawDown)
NewAvgDrawDown = Portfolio['NewDrawDown'].mean()
NewStdDrawDown = Portfolio['NewDrawDown'].std()

#Ratios // metrics
Portfolio['VXXDeltaWeight'] = Portfolio['NewAsset1Position'] / (
                 Portfolio['NewAsset1Position']+Portfolio['NewAsset2Position'])
Portfolio['ScaleFactor'] = (Portfolio['NewAsset1Position']+
                            Portfolio['NewAsset2Position'])
#Graphical display
Portfolio['NewLongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))    
