# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:08:47 2017

#pandas_datareader is deprecated use YahooGrabber
#This is part of a k-th fold optimization tool
"""
#lock and load
#import numpy as np
#from pandas_datareader import data
import pandas as pd
import time as t
import numpy as np
from pandas_datareader import data
from DefModADXStratOpt import DefModADXStratOpt
from ModADXAggMaker import ModADXAggMaker
#Get timeseries
ticker = 'TLT'
firsttime = '07/01/2002'
secondtime = '07/01/2007'
thirdtime = '07/01/2012'
fourthtime = '01/01/2015'
lasttime = '01/01/2050'
multiplier = 400
ranger1 = range(0,multiplier)
iterations = 5000
ranger2 = range(0,iterations) #Pass ranger2
empty = []
counter = 0
DS1W = pd.DataFrame()
DS2W = pd.DataFrame()
DS3W = pd.DataFrame()
DS4W = pd.DataFrame()
#number of iterations and sharpe threshold are defined in DefNormChaikinStratOpt
#this will correspond to DS1W
start1 = t.time()
s = data.DataReader(ticker, 'yahoo', start=firsttime, end=secondtime)
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
#the winners from each time period are in the sets below
for r in ranger1:
    print(counter)
    counter = counter + 1
    holder = DefModADXStratOpt(ranger2, s)
    DS1W = pd.concat([DS1W, holder], axis = 1)
end1 = t.time()
print('Dataset 1 is optimized, it took',end1-start1,'seconds') #run time in seconds
#this will correspond to DS2W
counter = 0
start2 = t.time()
s = data.DataReader(ticker, 'yahoo', start=secondtime, end=thirdtime)
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
for r in ranger1:
    print(counter)
    counter = counter + 1
    holder = DefModADXStratOpt(ranger2, s)
    DS2W = pd.concat([DS2W, holder], axis = 1)
end2 = t.time()
print('Dataset 2 is optimized, it took',end2-start2,'seconds') #run time in seconds
#Next
counter = 0
start3 = t.time()
s = data.DataReader(ticker, 'yahoo', start=thirdtime, end=lasttime)
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
for r in ranger1:
    print(counter)
    counter = counter + 1
    holder = DefModADXStratOpt(ranger2, s)
    DS3W = pd.concat([DS3W, holder], axis = 1)
end3 = t.time()
print('Dataset 3 is optimized, it took',end3-start3,'seconds')
#this will correspond to DS4W
counter = 0
start4 = t.time()
s = data.DataReader(ticker, 'yahoo', start=fourthtime, end=lasttime)
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
for r in ranger1:
    print(counter)
    counter = counter + 1
    holder = DefModADXStratOpt(ranger2, s)
    DS4W = pd.concat([DS4W, holder], axis = 1)
end4 = t.time()
print('Dataset 4 is optimized, it took',end4-start4,'seconds') #run time in seconds
#define off period test sets
S1TS = pd.DataFrame()
S2TS = pd.DataFrame()
S3TS = pd.DataFrame()
S4TS = pd.DataFrame()
#remove duplicate columns
DS1W = DS1W.loc[:,~DS1W.columns.duplicated()]
DS2W = DS2W.loc[:,~DS2W.columns.duplicated()]
DS3W = DS3W.loc[:,~DS3W.columns.duplicated()]
DS4W = DS4W.loc[:,~DS4W.columns.duplicated()]
#merge winners to create test sets
S1TS = pd.concat([S1TS, DS2W, DS3W, DS4W], axis = 1)
S2TS = pd.concat([S2TS, DS1W, DS3W, DS4W], axis = 1)
S3TS = pd.concat([S3TS, DS1W, DS2W, DS4W], axis = 1)
S4TS = pd.concat([S4TS, DS1W, DS2W, DS3W], axis = 1)
#dulpicates??
S1TS = S1TS.loc[:,~S1TS.columns.duplicated()]
S2TS = S2TS.loc[:,~S2TS.columns.duplicated()]
S3TS = S3TS.loc[:,~S3TS.columns.duplicated()]
S4TS = S4TS.loc[:,~S4TS.columns.duplicated()]
#test the test sets
testset1winners = ModADXAggMaker(ticker, S1TS, firsttime, secondtime)
testset2winners = ModADXAggMaker(ticker, S2TS, secondtime, thirdtime)
testset3winners = ModADXAggMaker(ticker, S3TS, thirdtime, lasttime)
testset4winners = ModADXAggMaker(ticker, S4TS, fourthtime, lasttime)
Aggregate = pd.DataFrame()
Aggregate = pd.concat([Aggregate, testset1winners, testset2winners,
                    testset3winners, testset4winners],axis = 1)
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
