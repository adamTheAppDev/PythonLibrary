# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a massive two asset portfolio tester with a brute force optimizer
#Takes all pair combos, tests, and sorts. 

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
#from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from ListPairs import ListPairs

#Empty data structures
Empty = []
Counter = 0
Counter2 = 0
Dataset2 = pd.DataFrame()

#Iterable 
iterations = range(0, 500)

#Start timer
Start = t.time()

#Assign tickers
tickers = ('TLT', 'SPY', 'TMF')#, 'AAPL', 'PBF', 'UVXY', '^VIX', 'GLD', 'SLV',
#           'JO','CORN', 'DBC', 'SOYB')

#Make all pairs in final list
MajorList = ListPairs(tickers)

#For all pairs in Brute Force Optimization
for m in MajorList:
    #Read in tickers
    Ticker1 = m[0]
    Ticker2 = m[1]
    #Combine tickers
    TAG = m[0] + '/' + m[1]
    #Create dataframes
    Dataset = pd.DataFrame()
    Portfolio = pd.DataFrame()
    
    #Request data
    Asset1 = YahooGrabber(Ticker1)
    Asset2 = YahooGrabber(Ticker2)    
   
    #Calculate log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
    Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
    
    #Time series trimmer
    trim = abs(len(Asset1) - len(Asset2))
    if len(Asset1) == len(Asset2):
        pass
    else:
        if len(Asset1) > len(Asset2):
            Asset1 = Asset1[trim:]
        else:
            Asset2 = Asset2[trim:]
    #For number of iterations
    for i in iterations:
        #Iteration tracking
        Counter = Counter + 1
        #Generate random params
        aa = rand.random() * 2 #uniformly distributed random number 0 to 2
        a = aa - 1          #a > 1 indicating long position in a
        bb = rand.random()
        if bb >= .5:
            bb = 1
        else:
            bb = -1
        b = bb * (1 - abs(a))

        #Change c and d to 0 by default if you want to just go flat
        #Generate random params
        cc = rand.random() * 2 #uniformly distributed random number 0 to 2
        c = cc - 1          #cc > 1 indicating long position in c
        dd = rand.random() * 2
        if dd >= 1:
            edd = 1
        else:
            edd = -1
        d = (dd - 1)
        #Constraint
        if abs(c) + abs(d) > 1:
            continue
        #Generate random params    
        e = rand.randint(3,25)
        f = rand.randint(3,25)
        #Assign params
        window = int(e)
        window2 = int(f)
        #Calculate moving averages
        Asset1['MA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
        Asset2['MA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()        
        #Position sizing
        Asset1['Position'] = a
        #Alternative position sizing
        Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['MA'].shift(1),
                                        c,a)         
        #Apply position to returns
        Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
        #Position sizing
        Asset2['Position'] = b
        #Alternative position sizing
        Asset2['Position'] = np.where(Asset2['Adj Close'].shift(1) > Asset2['MA'].shift(1),
                                        d,b)
        #Apply position to returns
        Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
        #Pass individual returns streams to portfolio
        Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position?
        Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position?
        #Portfolio returns
        Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
        #Constraints
        if Portfolio['LongShort'].std() == 0:    
            continue
        #Returns on $1
        Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
        #Incorrectly calculated max drawdown
        drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
        MaxDD = max(drawdown)
        #Constraint
        if MaxDD > float(.5): 
            continue
        #Performance metric
        dailyreturn = Portfolio['LongShort'].mean()
        #Constraint
        if dailyreturn < .0003:
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
        Empty.append(f)
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
    z1 = Dataset.iloc[7]
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
          r = Dataset.columns[(Dataset == j).iloc[7]]    
          #Add to dataframe
          DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
    #Top metric    
    y = max(z1)
    #Get column ID of metric
    k = Dataset.columns[(Dataset == y).iloc[7]]
    #Get column ID of metric - float
    kfloat = float(k[0])
    #End timer
    End = t.time()
    #Timer stats
    print(End-Start, 'seconds later')
    #Assign params
    Dataset[TAG] = Dataset[kfloat]
    Dataset2[TAG] = Dataset[TAG]
    #Rename columns
    Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
    #Iteration tracking
    Counter2 = Counter2 + 1
    #print(Dataset[TAG])
#Create dataframe        
Portfolio2 = pd.DataFrame()
#Metric of choice
z1 = Dataset2.iloc[7]
#Threshold
w1 = np.percentile(z1, 99)
v1 = [] #this variable stores the Nth percentile of top params
winners = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list   
      v1.append(h)
#For top metrics        
for j in v1:
      #Get column ID of metric
      r = Dataset2.columns[(Dataset2 == j).iloc[7]]    
      #Add to list
      winners = pd.concat([winners,Dataset2[r]], axis = 1)
#Top metric    
y = max(z1)
#Name of pair
k = Dataset2.columns[(Dataset2 == y).iloc[7]] 
#Name of pair - string
kfloat = str(k[0])

#Ticker names
num = kfloat.find('/')
num2 = num + 1

#Request data
Asset3 = YahooGrabber(kfloat[:num])
Asset4 = YahooGrabber(kfloat[num2:])    

#Time series trimmer
trim = abs(len(Asset3) - len(Asset4))
if len(Asset3) == len(Asset4):
    pass
else:
    if len(Asset3) > len(Asset4):
        Asset3 = Asset3[trim:]
    else:
        Asset4 = Asset4[trim:]

#Calculate log returns
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
Asset4['LogRet'] = np.log(Asset4['Adj Close']/Asset4['Adj Close'].shift(1))
Asset4['LogRet'] = Asset4['LogRet'].fillna(0)

#Read in params
window = int((Dataset2[kfloat][4]))
window2 = int((Dataset2[kfloat][5]))   

#Calculate moving averages
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
Asset4['MA'] = Asset4['Adj Close'].rolling(window=window2, center=False).mean()
#Position sizing
Asset3['Position'] = (Dataset2[k[0]][0])
#Alternative position sizing
Asset3['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset2[k[0]][2],Dataset2[k[0]][0])
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
#Position sizing
Asset4['Position'] = (Dataset2[kfloat][1])
#Alternative position sizing
Asset4['Position'] = np.where(Asset4['Adj Close'].shift(1) > Asset4['MA'].shift(1),
                                    Dataset2[k[0]][3],Dataset2[k[0]][1])
Asset4['Pass'] = (Asset4['LogRet'] * Asset4['Position'])

#Pass individual returns streams to portfolio
Portfolio2['Asset3Pass'] = Asset3['Pass'] #* (-1)
Portfolio2['Asset4Pass'] = Asset4['Pass'] #* (-1)
#Portfolio returns
Portfolio2['LongShort'] = Portfolio2['Asset3Pass'] + Portfolio2['Asset4Pass'] 
#Graphical display
Portfolio2['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio2['LongShort'].mean()
dailyvol = Portfolio2['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio2['Multiplier'] = Portfolio2['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
drawdown2 =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())
#Display results
print(kfloat)
print('--------')
print(Dataset2[kfloat])
#Incorrectly calculated max drawdown
print('Max Drawdown is ',max(drawdown2),'See Dataset2')
#Save to pickle
#pd.to_pickle(Portfolio, 'FileName')
