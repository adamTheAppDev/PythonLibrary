# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio tester with a brute force optimizer
#Takes all pair combos, tests, sorts, returns optimal params from all pairs + top performing pair params 

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
from pandas.parser import CParserError

#Empty data structure
Empty = []
Counter = 0
Counter2 = 0
Dataset2 = pd.DataFrame()

#Iterable
iterations = range(0, 100)

#Start timer
Start = t.time()

#Assign tickers
tickers = ('JNUG', 'TQQQ', 'TMF')#, 'AAPL', 'PBF', 'UVXY', '^VIX', 'TLT', 'SLV',
#           'JO','CORN', 'DBC', 'SOYB')

#Make all pairs in final list
MajorList = ListPairs(tickers)

#For every combination of tickers
for m in MajorList:
    #Ticker Assignment
    Ticker1 = m[0]
    Ticker2 = m[1]
    #Two ticker ID
    TAG = m[0] + '/' + m[1]
    #Clear dataframes
    Dataset = pd.DataFrame()
    Portfolio = pd.DataFrame()
    
    #Request data
    while True: 
        try:
            Asset1 = YahooGrabber(Ticker1)
            Asset2 = YahooGrabber(Ticker2)            
        except CParserError:
            continue
        break    
    
    #Calculate log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
    Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

    #Match time series lengths
    trim = abs(len(Asset1) - len(Asset2))
    if len(Asset1) == len(Asset2):
        pass
    else:
        if len(Asset1) > len(Asset2):
            Asset1 = Asset1[trim:]
        else:
            Asset2 = Asset2[trim:]
    #Brute force optimization
    for i in iterations:
        #Iteration tracking
        Counter = Counter + 1
        
        #Determining position and direction
        aa = rand.random() * 2 #uniformly distributed random number 0 to 2
        a = aa - 1             #a > 1 indicating long position in a
        bb = rand.random()
        if bb >= .5:
            bb = 1 #long
        else:
            bb = -1 #short
        b = bb * (1 - abs(a)) #long/short (1 - a)  

        #Change c and d to 0 by default to go flat - no exposure

        #Determining position and direction
        cc = rand.random() * 2 #uniformly distributed random number 0 to 2
        c = cc - 1             #c > 1 indicating long position in c
        dd = rand.random() * 2
        if dd >= 1:
            edd = 1 #long
        else:
            edd = -1 #short
        d = (dd - 1)
        if abs(c) + abs(d) > 1:
            continue
        
        #Moving average window assignment 
        e = rand.randint(3,20)
        window = int(e)
        
        #Price relative calculation
        Asset1['PriceRelative'] = Asset1['Adj Close']/Asset2['Adj Close']
        #Price relative moving average calculation
        Asset1['PRMA'] = Asset1['PriceRelative'].rolling(window=window, center=False).mean()

        #Position sizing
        Asset1['Position'] = a
        Asset1['Position'] = np.where(Asset1['PriceRelative'].shift(1) > Asset1['PRMA'].shift(1),
                                        c,a)
        #Apply position size to returns to pass to portfolio
        Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])

        #Position sizing       
        Asset2['Position'] = b
        Asset2['Position'] = np.where(Asset1['PriceRelative'].shift(1) > Asset1['PRMA'].shift(1),
                                        d,b)
        #Apply position size to returns to pass to portfolio
        Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

        #Pass position returns to portfolio
        Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position for long only position sizing
        Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position for long only position sizing

        #Add individual position returns to get portfolio returns
        Portfolio['Returns'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
        if Portfolio['Returns'].std() == 0:    
            continue
        
        #Returns on $1
        Portfolio['Multiplier'] = Portfolio['Returns'].cumsum().apply(np.exp)
        
        #Max drawdown calculation
        drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
        MaxDD = max(drawdown)
        
        #Optional max drawdown constraint
#        if MaxDD > float(.51): 
#            continue
        #Daily average return
        dailyreturn = Portfolio['Returns'].mean()
        #Optional Daily average return constraint
#        if dailyreturn < .0003:
#            continue
        #Daily standard deviation of returns
        dailyvol = Portfolio['Returns'].std()
        #Info/sharpe ratio
        sharpe =(dailyreturn/dailyvol)

        #Iteration tracking        
        print(Counter)

        #Saving params and metrics to table for sorting
        Empty.append(a)
        Empty.append(b)
        Empty.append(c)
        Empty.append(d)
        Empty.append(e)
        Empty.append(sharpe)
        Empty.append(sharpe/MaxDD)
        Empty.append(dailyreturn/MaxDD)
        Empty.append(MaxDD)
        Emptyseries = pd.Series(Empty)
        Dataset[0] = Emptyseries.values
        Dataset[i] = Emptyseries.values
        Empty[:] = [] 
        
    #Isolate sharpe/max drawdown metric
    z1 = Dataset.iloc[6]
    #Take cutoff for top 20% performers
    w1 = np.percentile(z1, 80)
    v1 = [] #this variable stores the Nth percentile of top performers
    DS1W = pd.DataFrame() #This variable stores params
    #Sorting/organizing
    for h in z1:
        if h > w1:
          v1.append(h)
    #Storing params in DS1W
    for j in v1:
          r = Dataset.columns[(Dataset == j).iloc[6]]    
          DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
    #top performing metric      
    y = max(z1)
    k = Dataset.columns[(Dataset == y).iloc[6]] #this is the column number that has top performing metric
    #Combo name
    kfloat = float(k[0])
    #End timer
    End = t.time()
    print(End-Start, 'seconds later')
    #Assignment
    Dataset[TAG] = Dataset[kfloat]
    Dataset2[TAG] = Dataset[TAG]
    #Column ID
    Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
    Counter2 = Counter2 + 1

#Final portfolio for top params        
Portfolio2 = pd.DataFrame()
#find top parameters
z1 = Dataset2.iloc[6]
w1 = np.percentile(z1, 99)
v1 = [] #this variable stores the Nth percentile of top performers
winners = pd.DataFrame() #this variable stores params

#Sorting
for h in z1:
    if h > w1:
      v1.append(h)
#Storing top params
for j in v1:
      r = Dataset2.columns[(Dataset2 == j).iloc[6]]    
      winners = pd.concat([winners,Dataset2[r]], axis = 1)
y = max(z1)
k = Dataset2.columns[(Dataset2 == y).iloc[6]] #this is the name of the top pair/combo
kfloat = str(k[0])

#TAG ID separation
num = kfloat.find('/')
num2 = num + 1

#Request data
while True: 
    try:
        Asset3 = YahooGrabber(kfloat[:num])
        Asset4 = YahooGrabber(kfloat[num2:])    
    except CParserError:
        continue
    break    

#Trim timeseries lengths to match
trim = abs(len(Asset3) - len(Asset4))
if len(Asset3) == len(Asset4):
    pass
else:
    if len(Asset3) > len(Asset4):
        Asset3 = Asset3[trim:]
    else:
        Asset4 = Asset4[trim:]

#Log return calculation
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
Asset4['LogRet'] = np.log(Asset4['Adj Close']/Asset4['Adj Close'].shift(1))
Asset4['LogRet'] = Asset4['LogRet'].fillna(0)

#MA window
window = int((Dataset2[kfloat][4]))

#Price relative calculation   
Asset3['PriceRelative'] = Asset3['Adj Close']/Asset4['Adj Close']
Asset3['PRMA'] = Asset3['PriceRelative'].rolling(window=window, center=False).mean()

#Position sizing from params
Asset3['Position'] = (Dataset2[k[0]][0])
Asset3['Position'] = np.where(Asset3['PriceRelative'].shift(1) > Asset3['PRMA'].shift(1),
                                    Dataset2[k[0]][2],Dataset2[k[0]][0])
#Apply position size to pass to portfolio
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])

#Position sizing from params
Asset4['Position'] = (Dataset2[kfloat][1])
Asset4['Position'] = np.where(Asset3['PriceRelative'].shift(1) > Asset3['PRMA'].shift(1),
                                    Dataset2[k[0]][3],Dataset2[k[0]][1])
#Apply position size to pass to portfolio
Asset4['Pass'] = (Asset4['LogRet'] * Asset4['Position'])

#Pass to portfolio
Portfolio2['Asset3Pass'] = Asset3['Pass']
Portfolio2['Asset4Pass'] = Asset4['Pass'] 
#Return calculation
Portfolio2['Returns'] = Portfolio2['Asset3Pass'] + Portfolio2['Asset4Pass'] 
#Plotting retuns
Portfolio2['Returns'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Portfolio statistics                                     
dailyreturn = Portfolio2['Returns'].mean()
dailyvol = Portfolio2['Returns'].std()
sharpe =(dailyreturn/dailyvol)
#Portfolio returns on $1
Portfolio2['Multiplier'] = Portfolio2['Returns'].cumsum().apply(np.exp)
#Portfolio drawdown
PortfolioDrawdown =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())

#Display results
print(kfloat)
print('--------')
print(Dataset2[kfloat])
print('Max Drawdown is ',max(PortfolioDrawdown),'See Dataset2')
