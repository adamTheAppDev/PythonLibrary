# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
import random as rand
import pandas as pd
import time as t
#from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from ListPairs import ListPairs
Empty = []
Start = t.time()
Counter = 0
Counter2 = 0
iterations = range(0, 200)
Dataset2 = pd.DataFrame()
#Input
tickers = ('TLT', 'SPY', 'TMF' 'AAPL', 'PBF', 'UVXY', '^VIX', 'GLD', 'SLV',
           'JO','CORN', 'DBC', 'SOYB')

#Make all pairs in final list
MajorList = ListPairs(tickers)

#Here we go

#Brute Force Optimization
for m in MajorList:
    Dataset = pd.DataFrame()
    Ticker1 = m[0]
    Ticker2 = m[1]
    TAG = m[0] + '/' + m[1]
    Dataset = pd.DataFrame()
    Portfolio = pd.DataFrame()
#pull online data, change to local for testing
    Asset1 = YahooGrabber(Ticker1)
    Asset2 = YahooGrabber(Ticker2)    
#get log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
    Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
#Match lengths
    trim = abs(len(Asset1) - len(Asset2))
    if len(Asset1) == len(Asset2):
        pass
    else:
        if len(Asset1) > len(Asset2):
            Asset1 = Asset1[trim:]
        else:
            Asset2 = Asset2[trim:]
#
    for i in iterations:
        Counter = Counter + 1
        aa = rand.random() * 2 #uniformly distributed random number 0 to 2
        a = aa - 1          #a > 1 indicating long position in a
        bb = rand.random()
        if bb >= .5:
            bb = 1
        else:
            bb = -1
        b = bb * (1 - abs(a))

#you can change c and d to 0 by default if you want to just go flat

        cc = rand.random() * 2 #uniformly distributed random number 0 to 2
        c = cc - 1          #cc > 1 indicating long position in c
        dd = rand.random() * 2
        if dd >= 1:
            edd = 1
        else:
            edd = -1
        d = (dd - 1)
        if abs(c) + abs(d) > 1:
            continue
        e = rand.randint(3,25)
        f = rand.randint(3,25)
        g = rand.randint(3,60)
        h = rand.randint(3,60)
        if g < e:
            continue
        if h < f:
            continue
        window = int(e)
        window2 = int(f)
        window3 = int(g)
        window3 = int(h)
        n = .1 - (rand.random())/5        
        o = .1 - (rand.random())/5       
        
        Asset1['smallSMA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
        Asset2['smallSMA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()
        Asset1['largeSMA'] = Asset1['Adj Close'].rolling(window=g, center=False).mean()
        Asset2['largeSMA'] = Asset2['Adj Close'].rolling(window=h, center=False).mean()        
        Asset1['SMAspread'] = Asset1['smallSMA'] - Asset1['largeSMA']
        Asset2['SMAspread'] = Asset2['smallSMA'] - Asset2['largeSMA']
        Asset1['Position'] = a
        Asset1['Position'] = np.where(Asset1['SMAspread'].shift(1) > n,
                                        c,a)                                    
        Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])

        Asset2['Position'] = b
        Asset2['Position'] = np.where(Asset2['SMAspread'].shift(1) > o,
                                        d,b)
        Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
        
        Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position?
        Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position?
        Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
        if Portfolio['LongShort'].std() == 0:    
            continue
        
        Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
        drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
        MaxDD = max(drawdown)
        if MaxDD > float(.5): 
            continue
        
        dailyreturn = Portfolio['LongShort'].mean()
        if dailyreturn < .0003:
            continue
        
        dailyvol = Portfolio['LongShort'].std()
        sharpe =(dailyreturn/dailyvol)
        
        Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
        drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
        MaxDD = max(drawdown)
        print(Counter)
        Empty.append(a)
        Empty.append(b)
        Empty.append(c)
        Empty.append(d)
        Empty.append(e)
        Empty.append(f)
        Empty.append(g)
        Empty.append(h)
        Empty.append(n)
        Empty.append(o)
        Empty.append(sharpe)
        Empty.append(sharpe/MaxDD)
        Empty.append(dailyreturn/MaxDD)
        Empty.append(MaxDD)
        Emptyseries = pd.Series(Empty)
        Dataset[0] = Emptyseries.values
        Dataset[i] = Emptyseries.values
        Empty[:] = [] 
#find optimal parameters from pair
    z1 = Dataset.iloc[11]
    w1 = np.percentile(z1, 80)
    v1 = [] #this variable stores the Nth percentile of top performers
    DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
    for l in z1:
        if l > w1:
          v1.append(l)
    for j in v1:
          r = Dataset.columns[(Dataset == j).iloc[11]]    
          DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
    y = max(z1)
    k = Dataset.columns[(Dataset == y).iloc[11]] #this is the column number
    kfloat = float(k[0])
    End = t.time()
    print(End-Start, 'seconds later')
    Dataset[TAG] = Dataset[kfloat]
    Dataset2[TAG] = Dataset[TAG]
    Dataset2 = Dataset2.rename(columns = {Counter2:TAG})
    Counter2 = Counter2 + 1
#    print(Dataset[TAG])
        
Portfolio2 = pd.DataFrame()
#find some winning parameters
z1 = Dataset2.iloc[11]
w1 = np.percentile(z1, 99)
v1 = [] #this variable stores the Nth percentile of top performers
winners = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for l in z1:
    if l > w1:
      v1.append(l)
for j in v1:
      r = Dataset2.columns[(Dataset2 == j).iloc[11]]    
      winners = pd.concat([winners,Dataset2[r]], axis = 1)
y = max(z1)
k = Dataset2.columns[(Dataset2 == y).iloc[11]] #this is the name of the pair
kfloat = str(k[0])

#most likely, you will want to export to csv for further future investigation

#print(Dataset[TAG])
num = kfloat.find('/')
num2 = num + 1
#you will need to re-call the Asset1 and Asset2 time series and log returns start here!!!
Asset3 = YahooGrabber(kfloat[:num])
Asset4 = YahooGrabber(kfloat[num2:])    

trim = abs(len(Asset3) - len(Asset4))
if len(Asset3) == len(Asset4):
    pass
else:
    if len(Asset3) > len(Asset4):
        Asset3 = Asset3[trim:]
    else:
        Asset4 = Asset4[trim:]

#get log returns
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
Asset4['LogRet'] = np.log(Asset4['Adj Close']/Asset4['Adj Close'].shift(1))
Asset4['LogRet'] = Asset4['LogRet'].fillna(0)

window = int((Dataset2[kfloat][4]))
window2 = int((Dataset2[kfloat][5]))   
window3 = int((Dataset2[kfloat][6]))
window4 = int((Dataset2[kfloat][7]))   

threshold = Dataset2[kfloat][8]
threshold2 = Dataset2[kfloat][9] 

Asset3['smallSMA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
Asset4['smallSMA'] = Asset4['Adj Close'].rolling(window=window2, center=False).mean()
Asset3['largeSMA'] = Asset3['Adj Close'].rolling(window=window3, center=False).mean()
Asset4['largeSMA'] = Asset4['Adj Close'].rolling(window=window4, center=False).mean()

Asset3['SMAspread'] = Asset3['smallSMA'] - Asset3['largeSMA']
Asset4['SMAspread'] = Asset4['smallSMA'] - Asset4['largeSMA']

Asset3['Position'] = (Dataset2[k[0]][0])
Asset3['Position'] = np.where(Asset3['SMAspread'].shift(1) > threshold,
                                    Dataset2[k[0]][2],Dataset2[k[0]][0])
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
Asset4['Position'] = (Dataset2[kfloat][1])
Asset4['Position'] = np.where(Asset4['SMAspread'].shift(1) > threshold,
                                    Dataset2[k[0]][3],Dataset2[k[0]][1])
Asset4['Pass'] = (Asset4['LogRet'] * Asset4['Position'])
#
Portfolio2['Asset3Pass'] = Asset3['Pass'] #* (-1)
Portfolio2['Asset4Pass'] = Asset4['Pass'] #* (-1)
Portfolio2['LongShort'] = Portfolio2['Asset3Pass'] + Portfolio2['Asset4Pass'] 
Portfolio2['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Portfolio2['LongShort'].mean()
dailyvol = Portfolio2['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio2['Multiplier'] = Portfolio2['LongShort'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio2['Multiplier'].div(Portfolio2['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
print(kfloat)
print('--------')
print(Dataset2[kfloat])
print('Max Drawdown is ',max(drawdown2),'See Dataset2')
##pd.to_pickle(Portfolio, 'VXX:UVXY')