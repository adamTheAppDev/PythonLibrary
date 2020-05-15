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
iterations = range(0, 10000)

#Start timer
Start = t.time()

#Assign tickers
tickers = ('TLT', 'SPY', 'TMF', 'AAPL', 'PBF', 'UVXY', '^VIX', 'GLD', 'SLV',
           'JO','CORN', 'DBC', 'SOYB')

#Make all pairs in final list
MajorList = ListPairs(tickers)

#For all pairs in Brute Force Optimization
for m in MajorList:
    #Read in tickers       
    Ticker1 = m[0]
    Ticker2 = m[1]
    #Create combined ticker name
    TAG = m[0] + '/' + m[1]
    #Empty dataframes
    Dataset = pd.DataFrame()
    Dataset2 = pd.DataFrame()
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

        #Can change c and d to 0 by default if you want to just go flat
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
        e = rand.randint(3,20)
        window = int(e)
        #Price relative
        Asset1['PriceRelative'] = Asset1['Adj Close']/Asset2['Adj Close']
        #Price relative moving average
        Asset1['PRMA'] = Asset1['PriceRelative'].rolling(window=window, center=False).mean()
        #Position sizing
        Asset1['Position'] = a
        #Alternative position sizing
        Asset1['Position'] = np.where(Asset1['PriceRelative'].shift(1) > Asset1['PRMA'].shift(1),
                                        c,a)        
        #Apply position to returns
        Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
        #Position sizing
        Asset2['Position'] = b
        #Alternative position sizing
        Asset2['Position'] = np.where(Asset1['PriceRelative'].shift(1) > Asset1['PRMA'].shift(1),
                                        d,b)
        #Apply position to returns
        Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
        #Pass individual return streams to portfolio
        Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position
        Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position
        #Cumulative portfolio returns   
        Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
        #Constraint   
        if Portfolio['LongShort'].std() == 0:    
            continue
        #Returns on $1
        Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
        #Incorrectly calculated max drawdown   
        drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
        MaxDD = max(drawdown)
        #Constraint
        if MaxDD > float(.51): 
            continue
        #Performance metric
        dailyreturn = Portfolio['LongShort'].mean()
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
    z1 = Dataset.iloc[6]
    #Threshold       
    w1 = np.percentile(z1, 80)
    v1 = [] #this variable stores the Nth percentile of top params
    DS1W = pd.DataFrame() #this variable stores your params for specific dataset
    #For all metrics       
    for h in z1:
        #If metric is greater than threshold              
        if h > w1:
          #Add to list            
          v1.append(h)
    #For top metrics       
    for j in v1:
          #Get column ID of metric            
          r = Dataset.columns[(Dataset == j).iloc[6]]    
          #Add to dataframe 
          DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
    #Top metric       
    y = max(z1)
    #Column ID of top metric       
    k = Dataset.columns[(Dataset == y).iloc[6]]
    #Column ID of top metric - float
    kfloat = float(k[0])
    #End timer       
    End = t.time()
    #Timer stats       
    print(End-Start, 'seconds later')
    #Assign params       
    Dataset[TAG] = Dataset[kfloat]       
    Dataset2[TAG] = Dataset[TAG]
    #Rename dataframe columns
    Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
    #Iteration tracking
    Counter2 = Counter2 + 1
    #print(Dataset[TAG])

#Create dataframe           
Portfolio2 = pd.DataFrame()
#Metric of choice
z1 = Dataset2.iloc[6]
#Threshold
w1 = np.percentile(z1, 99)
v1 = [] #this variable stores the Nth percentile of top params
winners = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than thresold       
    if h > w1:
      #Add to list                
      v1.append(h)
#For top metrics           
for j in v1:
      #Get column ID of metric     
      r = Dataset2.columns[(Dataset2 == j).iloc[6]]    
      #Add to dataframe     
      winners = pd.concat([winners,Dataset2[r]], axis = 1)
#Top metric           
y = max(z1)
#Pair name
k = Dataset2.columns[(Dataset2 == y).iloc[6]]
#Pair name - string
kfloat = str(k[0])

#Separate tickers in TAG
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

#Price relative
Asset3['PriceRelative'] = Asset3['Adj Close']/Asset4['Adj Close']
#Price relative moving average
Asset3['PRMA'] = Asset3['PriceRelative'].rolling(window=window, center=False).mean()

#Position sizing
Asset3['Position'] = (Dataset2[k[0]][0])
#Alternative position sizing
Asset3['Position'] = np.where(Asset3['PriceRelative'].shift(1) > Asset3['PRMA'].shift(1),
                                    Dataset2[k[0]][2],Dataset2[k[0]][0])
#Apply position to returns
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
#Position sizing
Asset4['Position'] = (Dataset2[kfloat][1])
#Alternative position sizing
Asset4['Position'] = np.where(Asset3['PriceRelative'].shift(1) > Asset3['PRMA'].shift(1),
                                    Dataset2[k[0]][3],Dataset2[k[0]][1])
#Apply position to returns
Asset4['Pass'] = (Asset4['LogRet'] * Asset4['Position'])

#Pass individual return streams to portfolio
Portfolio2['Asset3Pass'] = Asset3['Pass'] #* (-1)
Portfolio2['Asset4Pass'] = Asset4['Pass'] #* (-1)
#Price relative
Portfolio2['PriceRelative'] = Asset3['Adj Close'] / Asset3['Adj Close']
#Cumulative portfolio returns
Portfolio2['LongShort'] = Portfolio2['Asset3Pass'] + Portfolio2['Asset4Pass'] 

#Graphical display
Portfolio2['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))

#Performance metrics
dailyreturn = Portfolio2['LongShort'].mean()
dailyvol = Portfolio2['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio2['Multiplier'] = Portfolio2['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
drawdown2 =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())

#Display top param set + results
print(kfloat)
print('--------')
print(Dataset2[kfloat])
print('Max Drawdown is ',max(drawdown2),'See Dataset2')

#Save to pickle
#pd.to_pickle(Portfolio, 'FileName')
