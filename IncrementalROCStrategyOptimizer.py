# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimizer for a short only, martingale style, volatility trading strategy
#that takes incrementally larger positions

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Ticker assignment
Ticker1 = 'UVXY'
#Request data
Asset1 = DatabaseGrabber(Ticker1)
Asset1 = Asset1[:] #In
#Iterable
Iterations = range(0,50)
Counter = 1
#Range index 
Asset1['SubIndex'] = range(1,len(Asset1)+1)
#Empty data structures
Empty = []
Dataset = pd.DataFrame()
#For number of iterations in optimization
for n in Iterations:
    #Generate variable windows
    ROCWindow = rand.randint(5,200)
    HoldPeriod = rand.randint(25,200)
    ATRWindow = 20
    PositionSize = 1 + (rand.random() * 5) # 8 = 8% of account per leg
    UniformMove = rand.random() * .4 # .5 = 1.5 highoverrollingmin for first unit to be active
    PositionScale = rand.random() * .04 # .08 = add 8% to each new leg over previous leg
    #Log Returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    #ROC calculations
    Asset1['RateOfChange'] = (Asset1['Adj Close'] - Asset1['Adj Close'].shift(ROCWindow)
                                      ) / Asset1['Adj Close'].shift(ROCWindow)
    Bottom = Asset1['RateOfChange'].min()
    #Unit 1
    Asset1['UnitOne'] = 0
    Asset1['UnitOne'] = np.where(Asset1['RateOfChange'] > Bottom + (1 * UniformMove), PositionSize, 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitOne'] = np.where(Asset1['UnitOne'].shift(1) == PositionSize, PositionSize, Asset1['UnitOne'])
    #Unit 2
    Asset1['UnitTwo'] = 0
    Asset1['UnitTwo'] = np.where(Asset1['RateOfChange'] > Bottom + (2 * UniformMove), (PositionSize + (1 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitTwo'] = np.where(Asset1['UnitTwo'].shift(1) == (PositionSize + (1 * PositionScale)), (PositionSize + (1 * PositionScale)), Asset1['UnitTwo'])
    #Unit 3
    Asset1['UnitThree'] = 0
    Asset1['UnitThree'] = np.where(Asset1['RateOfChange'] > Bottom + (3 * UniformMove), (PositionSize + (2 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitThree'] = np.where(Asset1['UnitThree'].shift(1) == (PositionSize + (2 * PositionScale)), (PositionSize + (2 * PositionScale)), Asset1['UnitThree'])
    #Unit 4
    Asset1['UnitFour'] = 0
    Asset1['UnitFour'] = np.where(Asset1['RateOfChange'] > Bottom + (4 * UniformMove), (PositionSize + (3 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitFour'] = np.where(Asset1['UnitFour'].shift(1) == (PositionSize + (3 * PositionScale)), (PositionSize + (3 * PositionScale)), Asset1['UnitFour'])
    #Unit 5
    Asset1['UnitFive'] = 0
    Asset1['UnitFive'] = np.where(Asset1['RateOfChange'] > Bottom + (5 * UniformMove), (PositionSize + (4 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitFive'] = np.where(Asset1['UnitFive'].shift(1) == (PositionSize + (4 * PositionScale)), (PositionSize + (4 * PositionScale)), Asset1['UnitFive'])
    #Unit 6
    Asset1['UnitSix'] = 0
    Asset1['UnitSix'] = np.where(Asset1['RateOfChange'] > Bottom + (6 * UniformMove), (PositionSize + (5 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitSix'] = np.where(Asset1['UnitSix'].shift(1) == (PositionSize + (5 * PositionScale)), (PositionSize + (5 * PositionScale)), Asset1['UnitSix'])
    #Unit 7
    Asset1['UnitSeven'] = 0
    Asset1['UnitSeven'] = np.where(Asset1['RateOfChange'] > Bottom + (7 * UniformMove), (PositionSize + (6 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitSeven'] = np.where(Asset1['UnitSeven'].shift(1) == (PositionSize + (6 * PositionScale)), (PositionSize + (6 * PositionScale)), Asset1['UnitSeven'])
    #Unit 8
    Asset1['UnitEight'] = 0
    Asset1['UnitEight'] = np.where(Asset1['RateOfChange'] > Bottom + (8 * UniformMove), (PositionSize + (7 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitEight'] = np.where(Asset1['UnitEight'].shift(1) == (PositionSize + (7 * PositionScale)), (PositionSize + (7 * PositionScale)), Asset1['UnitEight'])
    #Unit 9
    Asset1['UnitNine'] = 0
    Asset1['UnitNine'] = np.where(Asset1['RateOfChange'] > Bottom + (9 * UniformMove), (PositionSize + (8 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitNine'] = np.where(Asset1['UnitNine'].shift(1) == (PositionSize + (8 * PositionScale)), (PositionSize + (8 * PositionScale)), Asset1['UnitNine'])
    #Unit 10
    Asset1['UnitTen'] = 0
    Asset1['UnitTen'] = np.where(Asset1['RateOfChange'] > Bottom + (10 * UniformMove), (PositionSize + (9 * PositionScale)), 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitTen'] = np.where(Asset1['UnitTen'].shift(1) == (PositionSize + (9 * PositionScale)), (PositionSize + (9 * PositionScale)), Asset1['UnitTen'])
    #Unit 11
    Asset1['UnitEleven'] = 0
    Asset1['UnitEleven'] = np.where(Asset1['RateOfChange'] > Bottom + (11 * UniformMove), PositionSize, 0)
    for i in range(0,HoldPeriod):
        Asset1['UnitEleven'] = np.where(Asset1['UnitEleven'].shift(1) == PositionSize, PositionSize, Asset1['UnitEleven'])
    
    #Adding position sizes
    Asset1['SumUnits'] = Asset1[['UnitOne','UnitTwo','UnitThree','UnitFour',#]].sum(axis = 1)
        'UnitFive','UnitSix','UnitSeven','UnitEight','UnitNine','UnitTen','UnitEleven']].sum(axis = 1)
    #Exposure methodology
    Asset1['Regime'] = np.where(Asset1['SumUnits'] >= 1, -1,0)
    #Apply weights to returns
    Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet'] * (Asset1['SumUnits']/100)
    #Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
    #                                 figsize=(8,5))
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    
    #Incorrectly calculated drawdown statistic
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
    #s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    
    #Iteration tracking
    Counter = Counter + 1
    #Constraints
    if MaxDD > .5:
        continue
    dailyreturn = Asset1['Strategy'].mean()
    if dailyreturn < .0015:
        continue
    dailyvol = Asset1['Strategy'].std()
    if dailyvol == 0:
        continue
    #Performance metrics    
    Sharpe = dailyreturn/dailyvol
    SharpeOverMaxDD = Sharpe/MaxDD
    #Save params and metrics to list
    Empty.append(ROCWindow)
    Empty.append(HoldPeriod)
    Empty.append(PositionSize)
    Empty.append(UniformMove)
    Empty.append(PositionScale)
    Empty.append(dailyreturn)
    Empty.append(dailyvol)
    Empty.append(Sharpe)
    Empty.append(SharpeOverMaxDD)
    Empty.append(MaxDD)
    #List to Series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe column
    Dataset[n] = Emptyseries.values
    #Clear list
    Empty[:] = []
    #Iteration tracking
    print(Counter)
   
#Rename columns
#Trades = Trades.rename(index={0: "ExitTaken", 1: "LengthOfTrade", 2: "EntryPriceUnitOne",
#                3: "StopPriceUnitOne", 4: "SubIndexOfEntry", 5: "SubIndexOfExit",
#                6: "TradeDirection", 7: "OpenPriceOnGap", 8: "TradeReturn"})
#Desired metric to sort
z1 = Dataset.iloc[7]
#Percentile threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If metric greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top metrics
for j in v1:
      #Find column ID 
      r = Dataset.columns[(Dataset == j).iloc[7]]
      #Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Optimal param
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[7]] #this is the column number
#Param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
#print(End-Start, 'seconds later')
#Display params
print(Dataset[k])
