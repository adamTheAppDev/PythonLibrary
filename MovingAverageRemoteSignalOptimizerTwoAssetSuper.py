# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimization, portfolio analysis tool, and trading strategy
#that has a reallocation based on drawdown - there may be some curve fitting

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
Dataset2 = pd.DataFrame()
Portfolio = pd.DataFrame()
Counter = 0

#Start timer
Start = t.time()

#Assign tickers 
Ticker1 = 'UVXY'
#Ticker2 = '^VIX'
Ticker3 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)
#Asset2 = YahooGrabber(Ticker2)

#Read in data
Asset2 = pd.read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\VX1CC.csv', sep = ',')
#Formatting
Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
Asset2 = Asset2.set_index('Date')
Asset2 = Asset2.reindex(index=Asset2.index[::-1])

#Time series trim
Asset1 = Asset1[:-6]

#Assign remote signal
Asset3 = Asset2
#Asset3 = YahooGrabber(Ticker3)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Time series trimmer
Asset3 = Asset3[-len(Asset2):]
#Asset2 = Asset2[-600:]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Primary Brute Force Optimization
#Number of iterations
iterations = range(0, 7500)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random variables
    a = rand.random()
    b = 1 - a
    c = 0#rand.random()
    d = 0#rand.random()
    #Constraint
    if c + d > 1:
        continue
    #Generate random variables
    e = rand.randint(3,30)
    window = int(e)
    #Calculate SMA
    Asset3['MA'] = Asset3['Close'].rolling(window=window, center=False).mean()
    Asset3['MA'] = Asset3['MA'].fillna(0)
    #Position sizing
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Asset3['Close'].shift(1) > Asset3['MA'].shift(1),
                                    c,a)    
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    Asset2['Position'] = np.where(Asset3['Close'].shift(1) > Asset3['MA'].shift(1),
                                    d,b)
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)#Pass a long position
    #Cumulative returns
    Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
    #Constraints
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown stat
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.3): 
        continue
    #Performance metrics
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metrics
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    
    #Iteration tracking
    print(Counter)
    #Save params and metrics to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
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
    
#Primary optimization output sorting
#Metric of choice
z1 = Dataset.iloc[6]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add metric to list
      v1.append(h)
#For all top metrics
for j in v1:
      #Find column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[6]]    
      #Add param set to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[6]] 
#Top param set
kfloat = float(k[0])
#End timer
End = t.time()

#Secondary optimization
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random variables
    f = rand.randint(31,252)
    g = rand.random() - .3
    #Constraint
    if g < .1:
        continue        
    window2 = int(f)
    #Calculate SMA
    Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
    Asset3['MA2'] = Asset3['MA2'].fillna(0)
    #Directional methodology
    Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
    #Signal
    Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] > Asset3['MA2'], 1, 0)
    #Volatility regime
    Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
    Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])
    #Regime change
    Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
    #Asset3['SignalReturns'].cumsum().apply(np.exp).plot()
    #Add'l returns
    Asset3['Super'] = (Asset3['SignalReturns'] * g ) + Portfolio['LongShort']
    #Returns on $1
    Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown stat
    SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
    SuperDrawdown = SuperDrawdown.fillna(0)
    SuperMaxDD = max(SuperDrawdown)
    #Performance metrics
    superdailyreturn = Asset3['Super'].mean()
    #Constraint
#    if dailyreturn > superdailyreturn:
#        continue
    #Performance metrics
    superdailyvol = Asset3['Super'].std()
    supersharpe =(superdailyreturn/superdailyvol)
    #Iteration tracking
    print(Counter)
    #Save params and metrics to list
    Empty.append(f)
    Empty.append(g)
    Empty.append(supersharpe)
    Empty.append(superdailyreturn)
    Empty.append(supersharpe/SuperMaxDD)
    Empty.append(superdailyreturn/SuperMaxDD)
    Empty.append(SuperMaxDD) 
    Empty.append(superdailyreturn)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset2[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
    
#Secondary optimization output sorting    
#Metric of choice
z2 = Dataset2.iloc[2]
#Threshold
w2 = np.percentile(z2, 80)
v2 = [] #this variable stores the Nth percentile of top params
DS2W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z2:
    #If greater than threshold
    if h > w1:
      #Add metric to list
      v2.append(h)
#For all top metrics
for j in v2:
      #Find column ID of metric
      r = Dataset2.columns[(Dataset2 == j).iloc[2]]    
      #Add param set to dataframe
      DS2W = pd.concat([DS2W,Dataset2[r]], axis = 1)
#Top metric
y2 = max(z2)
#Column ID of top metric
k2 = Dataset2.columns[(Dataset2 == y2).iloc[2]]
#Top param set
k2float = float(k2[0])
#End timer
End2 = t.time()

#Timer stats
print(End2-Start, 'seconds later')
#Display top metrics
print('Dataset[k]')
print(Dataset[k])
print('Dataset2[k2]')
print(Dataset2[k2])    
    
#Read top metrics into model
window = int((Dataset[kfloat][4]))
window2 = int((Dataset2[k2float][0]))
#Calculate SMA
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()   
Asset3['MA'] = Asset3['MA'].fillna(0)
Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
Asset3['MA2'] = Asset3['MA2'].fillna(0)
#Position sizing
Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1) #Pass a short position
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)#Pass a long position
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Total returns
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown stat
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
print(max(drawdown2))
#Directional methogology
Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] < Asset3['MA2'], 1, 0)
#Volatility regime
Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])
#Regime change
Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
#Asset3['SignalReturns'].cumsum().apply(np.exp).plot()
#Leverage factor
SuperFactor = Dataset2[k2float][1]
#Applied to portfolio returns
Asset3['Super'] = (Asset3['SignalReturns'] * SuperFactor) + Portfolio['LongShort']
#Returns on $1
Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown stat
SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
SuperDrawdown = SuperDrawdown.fillna(0)
SuperMaxDD = max(SuperDrawdown)
#Performance metrics
superdailyreturn = Asset3['Super'].mean()
superdailyvol = Asset3['Super'].std()
supersharpe =(superdailyreturn/superdailyvol)
#Incorrectly calculated max drawdown stat
print(SuperMaxDD)
Asset3['SuperMultiplier'][:].plot()
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Optional save to pickle
#pd.to_pickle(Portfolio, 'VXX:UVXY')
