# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:08:47 2017

@author: AmatVictoriaCuramIII
"""
#lock and load
#import numpy as np
#from pandas_datareader import data
import pandas as pd
import time as t
from DefNormChaikinStratOpt import DefNormChaikinStratOpt
from ChaikinAggMaker import ChaikinAggMaker
#Get timeseries
ticker = '^GSPC'
firsttime = '07/01/1983'
secondtime = '01/01/1995'
thirdtime = '01/01/2006'
fourthtime = '01/01/2010'
lasttime = '01/01/2050'
#number of iterations and sharpe threshold are defined in DefNormChaikinStratOpt
#this will correspond to DS1W
start1 = t.time()
#the winners from each time period are in the sets below
DS1W = DefNormChaikinStratOpt(ticker, firsttime, secondtime)
end1 = t.time()
print('Dataset 1 is optimized, it took',end1-start1,'seconds') #run time in seconds
#this will correspond to DS2W
start2 = t.time()
DS2W = DefNormChaikinStratOpt(ticker, secondtime, thirdtime)
end2 = t.time()
print('Dataset 2 is optimized, it took',end2-start2,'seconds') #run time in seconds
start3 = t.time()
DS3W = DefNormChaikinStratOpt(ticker, thirdtime, lasttime)
end3 = t.time()
print('Dataset 3 is optimized, it took',end3-start3,'seconds')
#this will correspond to DS4W
start4 = t.time()
DS4W = DefNormChaikinStratOpt(ticker, fourthtime, lasttime)
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
#test the test sets
testset1winners = ChaikinAggMaker(ticker, S1TS, firsttime, secondtime)
testset2winners = ChaikinAggMaker(ticker, S2TS, secondtime, thirdtime)
testset3winners = ChaikinAggMaker(ticker, S3TS, thirdtime, lasttime)
testset4winners = ChaikinAggMaker(ticker, S4TS, fourthtime, lasttime)
Aggregate = pd.DataFrame()
Aggregate = pd.concat([Aggregate, testset1winners, testset2winners,
                    testset3winners, testset4winners],axis = 1)
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]