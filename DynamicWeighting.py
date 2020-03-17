# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset weighting/testing tool, it has a reallocation
#method based on drawdown which may not be suitable for real life application
#Probably some curve fitting going on here.

#Dynamic Weighting

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber 
#from YahooGrabber import YahooGrabberII 

#Variable assignment
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Assign tickers
Ticker1 = 'UVXY' #Short Position
Ticker2 = 'VXX' #Long Position

#Grab local data, or..
Asset1 = DatabaseGrabber(Ticker1)
Asset2 = DatabaseGrabber(Ticker2)

#Request data
#Asset1 = YahooGrabber()
#Asset2 = YahooGrabber()

#Trimmer to match time series lengths
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Out/in of sample trimmer
#Asset1 = Asset1[-100:]
#Asset2 = Asset2[-100:]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Brute Force Optimization
#Number of iterations
#iterations = range(0, 10000)
#For number of iterations
#for i in iterations:
#    #Iteration tracking
#    Counter = Counter + 1
#    #random param generation
#    a = rand.random()
#    b = 1 - a
#    c = rand.random()
#    d = rand.random()
#    e = rand.random()
#    f = rand.random()
#    g = rand.random()
#    h = rand.random()   

#Position size assignment
Asset1['Position'] = .4#a
#Apply returns to position size
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position size assignment
Asset2['Position'] = .6#b
#Apply returns to position size
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Variable assignment (not vectorized)
Asset1Position = .4#a
Asset2Position = .6#b
#Pass position size to portfolio
Portfolio['Asset1Pass'] = (Asset1['Pass']) 
Portfolio['Asset2Pass'] = (Asset2['Pass'])
#Combine weighted returns into strategy
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] * -1) + (Portfolio['Asset2Pass']) #Pass a short position
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Performance statistics
DailyReturn = Portfolio['LongShort'].mean()
#    #Constraints
#    if dailyreturn < .0015:
#        continue
#Performance statistics
DailyVol = Portfolio['LongShort'].std()
#   #Constraints
#   if Portfolio['LongShort'].std() == 0:    
#        continue
#Performance statistics
Sharpe = (DailyReturn/DailyVol)
#Incorrectly calculated drawdown calculation
DrawDown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#Wrong
Portfolio['DrawDown'] = DrawDown
#Bad
MaxDD = max(DrawDown)
#Spurious
AvgDrawDown = Portfolio['DrawDown'].mean()
StdDrawDown = Portfolio['DrawDown'].std()

#Graph
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))

#New Allocation based on regime change
Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'] > (AvgDrawDown + #c (+/-c*StdDrawDown), 
                StdDrawDown), (Asset1Position + -.19), Asset1['Position']) #d
Portfolio['NewAsset2Position'] = np.where(Portfolio['DrawDown'] > (AvgDrawDown + #e (AvgDrawDown (+/-e*StdDrawDown)), 
                StdDrawDown), (Asset2Position + .16), Asset2['Position']) #f

#New asset return streams with regime change implemented
Portfolio['Asset1NewPass'] = (Asset1['LogRet'] * Portfolio['NewAsset1Position'])                            
Portfolio['Asset2NewPass'] = (Asset2['LogRet'] * Portfolio['NewAsset2Position'])
#New portfolio return stream with regime change implemented
Portfolio['NewLongShort'] = (Portfolio['Asset1NewPass'] * -1) + (Portfolio['Asset2NewPass']) #Pass a short position
#Portfolio returns on $1
Portfolio['NewMultiplier'] = Portfolio['NewLongShort'].cumsum().apply(np.exp)

#Perfomance metrics
NewDailyReturn = Portfolio['NewLongShort'].mean()
#    #Constraint
#    if dailyreturn < .0015:
#        continue
#Perfomance metrics
NewDailyVol = Portfolio['NewLongShort'].std()
#    #Constraint
#   if Portfolio['NewLongShort'].std() == 0:    
#        continue
#Perfomance metrics
NewSharpe =(NewDailyReturn/(NewDailyVol))

#Incorrectly calculated drawdown stat - pls fix
NewDrawDown =  1 - Portfolio['NewMultiplier'].div(Portfolio['NewMultiplier'].cummax())
Portfolio['NewDrawDown'] = NewDrawDown
NewMaxDD = max(NewDrawDown)
NewAvgDrawDown = Portfolio['NewDrawDown'].mean()
NewStdDrawDown = Portfolio['NewDrawDown'].std()

#Graphical display
Portfolio['NewLongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
