# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#The structure here is abominable, but this is a portfolio analysis tool 
#based on price relative info
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
#Number of iterations
iterations = range(0,50)
#Empty structures
empty = []
asone = pd.DataFrame()
start = t.time()
dataset = pd.DataFrame()
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
#Position sizing
UVXY['Position'] = .01
UVXY['Pass'] = UVXY['LogRet'] * UVXY['Position']
VXX['Position'] = .9
VXX['Pass'] = VXX['LogRet'] * VXX['Position']
VIX['Position'] = .5
VIX['Pass'] = VIX['LogRet'] * VIX['Position']
VXV['Position'] = .5
VXV['Pass'] = VXV['LogRet'] * VXV['Position']
TLT['Position'] = .5
TLT['Pass'] = TLT['LogRet'] * TLT['Position']
#New dataframe
asone['VXXpass'] = VXX['Pass']
asone['UVXYpass'] = UVXY['Pass']
#Price relative calculation
asone['PriceRelative'] = VXX['Adj Close'] / UVXY['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
#Portfolio returns
asone['LongShort'] = (-1 * VXX['Pass']) + (UVXY['Pass']) 
#Time series trimmmer
asone = asone[:-2]
#Grahpical display
asone['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = asone['LongShort'].mean()
dailyvol = asone['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
#Ones + zeros
maxdd = 0
tempdd = 0 
highwater = 1
#Incorrectly calculated max drawdown statistic
ranger = range(0,len(portfoliomultiplier))
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
#Incorrect        
print(maxdd)
#Correlation dataframe    
correl =  pd.DataFrame()
correl['VXX'] = VXX['Pass']
correl['UVXY'] = UVXY['Pass']
#print(correl.corr())
#Performance metric
wannabecorr = correl['VXX'].rolling(window = 40).corr(correl['UVXY'])
