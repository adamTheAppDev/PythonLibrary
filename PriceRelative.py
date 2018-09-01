# -*- coding: utf-8 -*-
"""
Created on Sat May 13 01:28:14 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
iterations = range(0,50)
empty = []
asone = pd.DataFrame()
start = t.time()
dataset = pd.DataFrame()
UVXY = DatabaseGrabber('UVXY')
VXX = DatabaseGrabber('VXX')
VIX = DatabaseGrabber('^VIX')
VXV = DatabaseGrabber('^VXV')
TLT = DatabaseGrabber('TLT')

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
UVXY =  UVXY[:-7]
VXX = VXX[-(len(UVXY)):]
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
asone['VXXpass'] = VXX['Pass']
asone['UVXYpass'] = UVXY['Pass']
asone['PriceRelative'] = VXX['Adj Close'] / UVXY['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
asone['LongShort'] = (-1 * VXX['Pass']) + (UVXY['Pass']) 
asone = asone[:-2]
asone['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = asone['LongShort'].mean()
dailyvol = asone['LongShort'].std()
sharpe =(dailyreturn/dailyvol)

portfoliomultiplier = asone['LongShort'].cumsum().apply(np.exp)
maxdd = 0
tempdd = 0 
highwater = 1
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
        
print(maxdd)
    
    
correl =  pd.DataFrame()
correl['VXX'] = VXX['Pass']
correl['UVXY'] = UVXY['Pass']
#print(correl.corr())
wannabecorr = correl['VXX'].rolling(window = 40).corr(correl['UVXY'])





























#s3['Position'] = .5
#s3['Pass'] = s3['LogRet'] * s3['Position']
#s4['LogRet'] = np.log(s4['Adj Close']/s4['Adj Close'].shift(1))
#s4['LogRet'] = s4['LogRet'].fillna(0)
#s4['Position'] = .5
#s4['Pass'] = s4['LogRet'] * s4['Position']
#trim = len(s3) - len(s4)
#s3 = s3[trim:]
#s3['Meter'] = s['Close']/s2['Close']
#s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1))
#s3['LogRet'] = s3['LogRet'].fillna(0)
#s3['Meter'] = s['Close']/s2['Close']
#s3['Meter'].plot(grid=True, figsize=(8, 5))
#s3['Touch'] = np.where(s3['Meter'] < 2, -1, 0) # short signal
#s3['Touch'] = np.where(s3['Meter'] > 1.048121, 1, s3['Touch']) #flat signal
#s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0) #short
#s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1, #stays
#                                     s3['Sustain']) #short
#s3['Sustain'] = np.where(s3['Touch'].shift(1) == 0, 0, 0) #flat
#s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 0, 0, #stays
#                                     s3['Sustain']) #flat
##    s3['Sustain'] = np.where(s3['Meter'] < .8, 0, s3['Sustain']) #cover short
#s3['Regime'] = s3['Touch'] + s3['Sustain']
#s3['Strategy'] = ((s3['Regime']).shift(1)*s3['Pass']*-1) + ((s3['Regime']
#                                ).shift(1)*s4['Pass'])
#s3['Strategy'] = s3['Strategy'].fillna(0)
#s3['NegLogReturns'] = s3['LogRet'] * -1  
#s3['ShortReturns'] = (s3['Pass']) + (s4['Pass']*-1)
#sharpe = (s3['Strategy'].mean()-s3['ShortReturns'].mean())/s3['Strategy'].std()
#print(sharpe)
#s3[['NegLogReturns', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
#                                                figsize=(8, 5))