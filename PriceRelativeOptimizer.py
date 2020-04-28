# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a portfolio analysis tool with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber

#Empty data strucutres
empty = []
dataset = pd.DataFrame()
asone = pd.DataFrame()
start = t.time()
counter = 0

#Request data
UVXY = DatabaseGrabber('UVXY')
VXX = DatabaseGrabber('VXX')
VIX = DatabaseGrabber('^VIX')
VXV = DatabaseGrabber('^VXV')
TLT = DatabaseGrabber('TLT')

#Calculate log returns
UVXY['LogRet'] = np.log(UVXY['Adj Close']/UVXY['Adj Close'].shift(1))
UVXY['LogRet'] = UVXY['LogRet'].fillna(0)
VXX['LogRet'] = np.log(VXX['Adj Close']/VXX['Adj Close'].shift(1))
VXX['LogRet'] = VXX['LogRet'].fillna(0)
VIX['LogRet'] = np.log(VIX['Adj Close']/VIX['Adj Close'].shift(1))
VIX['LogRet'] = VIX['LogRet'].fillna(0)
VXV['LogRet'] = np.log(VXV['Adj Close']/VXV['Adj Close'].shift(1))
VXV['LogRet'] = VXV['LogRet'].fillna(0)
TLT['LogRet'] = np.log(TLT['Adj Close']/TLT['Adj Close'].shift(1))
TLT['LogRet'] = TLT['LogRet'].fillna(0)

#Time series trimmer
UVXY =  UVXY[:-7]
VXX = VXX[-(len(UVXY)):]
VXX = VXX[:-1]
#Number of iterations
iterations = range(0, 500)
#For number of iterations
for i in iterations:
    #Iteration tracking
    counter = counter + 1
    #Generate random params
    a = rand.random()
    b = 1 - a
    #Position sizing // apply position to returns
    UVXY['Position'] = a
    UVXY['Pass'] = UVXY['LogRet'] * UVXY['Position']
    VXX['Position'] = b
    VXX['Pass'] = VXX['LogRet'] * VXX['Position']
    VIX['Position'] = .5
    VIX['Pass'] = VIX['LogRet'] * VIX['Position']
    VXV['Position'] = .5
    VXV['Pass'] = VXV['LogRet'] * VXV['Position']
    TLT['Position'] = .5
    TLT['Pass'] = TLT['LogRet'] * TLT['Position']
    asone['VXXpass'] = VXX['Pass']
    asone['UVXYpass'] = UVXY['Pass']
    #Price relative calculation
    asone['PriceRelative'] = VXX['Adj Close'] / UVXY['Adj Close']
    #asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
    #Combine returns
    asone['LongShort'] = UVXY['Pass'] + (-1 * VXX['Pass']) 
#    asone = asone[:-2]
#    asone['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    #Performance metric
    dailyreturn = asone['LongShort'].mean()
    dailyvol = asone['LongShort'].std()
    #Constraints
    if asone['LongShort'].std() == 0:    
        continue
    #Performance metric
    sharpe =(dailyreturn/(dailyvol))
    #Constraints
    if sharpe < 0.042:     
        continue
    #Returns on $1
    portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
    #Zeros, ones
    maxdd = 0
    tempdd = 0 
    highwater = 1
    #Iterable
    ranger = range(0,len(portfoliomultiplier))
    #For periods in time series - set high water mark
    for r in ranger:
        currentvalue = portfoliomultiplier[r]
        if highwater == 0:
            currentvalue = highwater
        if currentvalue > highwater:
            highwater = currentvalue
        else:
            tempdd = 1 - (currentvalue/highwater)
        #Set max drawdown    
        if tempdd > maxdd:
            maxdd = tempdd
            tempdd = 0
    #Iteration tracking        
    print(counter)    
    empty.append(a)
    empty.append(b)
    empty.append(sharpe)
    empty.append(sharpe/maxdd)
    #List to series
    emptyseries = p.Series(empty)
    #Series to dataframe
    dataset[i] = emptyseries.values
    #Clear list
    empty[:] = [] 
#Metric of choice    
z1 = dataset.iloc[3]
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
      #Get column ID of top metric    
      r = dataset.columns[(dataset == j).iloc[3]]  
      #Add to dataframe
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = dataset.columns[(dataset == y).iloc[3]] 
#Top param set
kfloat = float(k[0])
#End timer
end = t.time()
#Timer stats
print(end-start, 'seconds later')
#Top param set
print(dataset[k])

#Read in top params
#Position sizing // apply position to returns
UVXY['Position'] = (dataset[kfloat][0])/2
UVXY['Pass'] = UVXY['LogRet'] * UVXY['Position']
VXX['Position'] = (dataset[kfloat][1])/2
VXX['Pass'] = VXX['LogRet'] * VXX['Position']
VIX['Position'] = .5
VIX['Pass'] = VIX['LogRet'] * VIX['Position']
VXV['Position'] = .5
VXV['Pass'] = VXV['LogRet'] * VXV['Position']
TLT['Position'] = .5
TLT['Pass'] = TLT['LogRet'] * TLT['Position']
#Pass returns to portfolio
asone['VXXpass'] = VXX['Pass']
asone['UVXYpass'] = UVXY['Pass']
#Calculate price relative
asone['PriceRelative'] = VXX['Adj Close'] / UVXY['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
#Combine returns
asone['LongShort'] = UVXY['Pass'] + (-1 * VXX['Pass']) 
#Time series trim
asone = asone[:-2]
#Display portfolio returns
asone['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metric
dailyreturn = asone['LongShort'].mean()
dailyvol = asone['LongShort'].std()
sharpe =(dailyreturn)
portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
#Zeros, ones
maxdd = 0
tempdd = 0 
highwater = 1
ranger = range(0,len(portfoliomultiplier))
#For all periods in time series - calculate high water mark + max drawdown
for r in ranger:
    currentvalue = portfoliomultiplier[r]
    if highwater == 0:
        currentvalue = highwater
    if currentvalue > highwater:
        highwater = currentvalue
    else:
        tempdd = 1 - (currentvalue/highwater)
    if tempdd > maxdd:
        maxdd = tempdd
        tempdd = 0
#Display results
print('Max drawdown is ' + str(maxdd))
