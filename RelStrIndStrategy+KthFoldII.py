# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:00:21 2017

@author: AmatVictoriaCuramIII
"""

#This is the middle part of a kth fold optimization tool
#Its definitely written out the long way
#pandas_datareader is deprecated, use YahooGrabber

#from pandas_datareader import data
import numpy as np
import pandas as pd
import time as t
def RelStrIndTester(s1, s2, s3, s4, testset1, testset2, testset3, testset4):
    testset1winners = pd.DataFrame()
    testset2winners = pd.DataFrame()
    testset3winners = pd.DataFrame()
    testset4winners = pd.DataFrame()   
    np.seterr(divide='ignore', invalid='ignore')
    start1 = t.time()
    testset1 = testset1.loc[:,~testset1.columns.duplicated()]
    testset2 = testset2.loc[:,~testset2.columns.duplicated()]
    testset3 = testset3.loc[:,~testset3.columns.duplicated()]
    testset4 = testset4.loc[:,~testset4.columns.duplicated()]
    for i in testset1:
        a = testset1[i].iloc[0]
        aa = a.astype(int)
        b = testset1[i].iloc[1]
        c = testset1[i].iloc[2]
        d = testset1[i].iloc[3]
        e = testset1[i].iloc[4]
        openspace = []
        openseries = pd.Series()
        s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1)) 
        s1['LogRet'] = s1['LogRet'].fillna(0)
        close = s1['Adj Close']
        window = aa
        delta = close.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        AvgGain = up.rolling(window).mean()
        AvgLoss = down.abs().rolling(window).mean() 
        RS = AvgGain/AvgLoss
        RSI = 100 - (100/(1.0+RS))
        s1['RSI'] = RSI
        s1['RSI'] = s1['RSI'].fillna(0)
        s1['Touch'] = np.where(s1['RSI'] < b, 1, 0) #long signal
        s1['Touch'] = np.where(s1['RSI'] > c, -1, s1['Touch']) #short signal
        s1['Sustain'] = np.where(s1['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s1['Sustain'] = np.where(s1['Sustain'].shift(1) == 1, 1, 
                                   s1['Sustain']) 
        s1['Sustain'] = np.where(s1['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s1['Sustain'] = np.where(s1['Sustain'].shift(1) == -1, -1,
                                   s1['Sustain']) 
        s1['Sustain'] = np.where(s1['RSI'] > d, 0, s1['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s1['Sustain'] = np.where(s1['RSI'] < e, 0, s1['Sustain']) #never actually true when optimized
        s1['Regime'] = s1['Touch'] + s1['Sustain']
        s1['Strategy'] = (s1['Regime'][window:]).shift(1)*s1['LogRet'][window:]
        s1['Strategy'] = s1['Strategy'].fillna(0)
        endgains = 1
        endreturns = 1
        for g in s1['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s1['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        if endreturns > endgains:
            continue       
        if s1['Strategy'].std() == 0:
            continue
        sharpe = (s1['Strategy'].mean()-abs(s1['LogRet'].mean()))/s1['Strategy'].std()
        if sharpe < .035:
            continue
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        openseries = pd.Series(openspace)
        testset1winners[i] = openseries.values
        openspace[:] = []
    end1 = t.time()
    print('Datasets were tested in time 1, it took',end1-start1,'seconds')
    start2 = t.time()
    for i in testset2:
        a = testset2[i].iloc[0]
        aa = a.astype(int)
        b = testset2[i].iloc[1]
        c = testset2[i].iloc[2]
        d = testset2[i].iloc[3]
        e = testset2[i].iloc[4]
        openspace = []
        openseries = pd.Series()
        s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1)) 
        s2['LogRet'] = s2['LogRet'].fillna(0)
        close = s2['Adj Close']
        window = aa  
        delta = close.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        AvgGain = up.rolling(window).mean()
        AvgLoss = down.abs().rolling(window).mean() 
        RS = AvgGain/AvgLoss
        RSI = 100 - (100/(1.0+RS))
        s2['RSI'] = RSI
        s2['RSI'] = s2['RSI'].fillna(0)
        s2['Touch'] = np.where(s2['RSI'] < b, 1,0) #long signal
        s2['Touch'] = np.where(s2['RSI'] > c, -1, s2['Touch']) #short signal
        s2['Sustain'] = np.where(s2['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s2['Sustain'] = np.where(s2['Sustain'].shift(1) == 1, 1, 
                                   s2['Sustain']) 
        s2['Sustain'] = np.where(s2['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s2['Sustain'] = np.where(s2['Sustain'].shift(1) == -1, -1,
                                   s2['Sustain']) 
        s2['Sustain'] = np.where(s2['RSI'] > d, 0, s2['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s2['Sustain'] = np.where(s2['RSI'] < e, 0, s2['Sustain']) #never actually true when optimized
        s2['Regime'] = s2['Touch'] + s2['Sustain']
        s2['Strategy'] = (s2['Regime'][window:]).shift(1)*s2['LogRet'][window:]
        s2['Strategy'] = s2['Strategy'].fillna(0)
        endgains = 1
        endreturns = 1
        for g in s2['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s2['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        if endreturns > endgains:
            continue  
        if s2['Strategy'].std() == 0:
            continue
        sharpe = (s2['Strategy'].mean()-abs(s2['LogRet'].mean()))/s2['Strategy'].std()
        if sharpe < .035:
            continue
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        openseries = pd.Series(openspace)
        testset2winners[i] = openseries.values
        openspace[:] = []
    end2 = t.time()
    print('Datasets were tested in time 2, it took',end2-start2,'seconds')
    start3 = t.time()
    for i in testset3:
        a = testset3[i].iloc[0]
        aa = a.astype(int)
        b = testset3[i].iloc[1]
        c = testset3[i].iloc[2]
        d = testset3[i].iloc[3]
        e = testset3[i].iloc[4]
        openspace = []
        openseries = pd.Series()
        s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1)) 
        s3['LogRet'] = s3['LogRet'].fillna(0)
        close = s3['Adj Close']
        window = aa  
        delta = close.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        AvgGain = up.rolling(window).mean()
        AvgLoss = down.abs().rolling(window).mean() 
        RS = AvgGain/AvgLoss
        RSI = 100 - (100/(1.0+RS))
        s3['RSI'] = RSI
        s3['RSI'] = s3['RSI'].fillna(0)
        s3['Touch'] = np.where(s3['RSI'] < b, 1,0) #long signal
        s3['Touch'] = np.where(s3['RSI'] > c, -1, s3['Touch']) #short signal
        s3['Sustain'] = np.where(s3['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s3['Sustain'] = np.where(s3['Sustain'].shift(1) == 1, 1, 
                                   s3['Sustain']) 
        s3['Sustain'] = np.where(s3['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s3['Sustain'] = np.where(s3['Sustain'].shift(1) == -1, -1,
                                   s3['Sustain']) 
        s3['Sustain'] = np.where(s3['RSI'] > d, 0, s3['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s3['Sustain'] = np.where(s3['RSI'] < e, 0, s3['Sustain']) #never actually true when optimized
        s3['Regime'] = s3['Touch'] + s3['Sustain']
        s3['Strategy'] = (s3['Regime'][window:]).shift(1)*s3['LogRet'][window:]
        s3['Strategy'] = s3['Strategy'].fillna(0)
        endgains = 1
        endreturns = 1
        for g in s3['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s3['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        if endreturns > endgains:
            continue     
        if s3['Strategy'].std() == 0:
            continue
        sharpe = (s3['Strategy'].mean()-abs(s3['LogRet'].mean()))/s3['Strategy'].std()
        if sharpe < .035:
            continue
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        openseries = pd.Series(openspace)
        testset3winners[i] = openseries.values
        openspace[:] = []
    end3 = t.time()
    print('Datasets were tested in time 3, it took',end3-start3,'seconds')    
    start4 = t.time()    
    for i in testset4:
        a = testset4[i].iloc[0]
        aa = a.astype(int)
        b = testset4[i].iloc[1]
        c = testset4[i].iloc[2]
        d = testset4[i].iloc[3]
        e = testset4[i].iloc[4]
        openspace = []
        openseries = pd.Series()
        s4['LogRet'] = np.log(s4['Adj Close']/s4['Adj Close'].shift(1)) 
        s4['LogRet'] = s4['LogRet'].fillna(0)
        close = s4['Adj Close']
        window = aa  
        delta = close.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        AvgGain = up.rolling(window).mean()
        AvgLoss = down.abs().rolling(window).mean() 
        RS = AvgGain/AvgLoss
        RSI = 100 - (100/(1.0+RS))
        s4['RSI'] = RSI
        s4['RSI'] = s4['RSI'].fillna(0)
        s4['Touch'] = np.where(s4['RSI'] < b, 1,0) #long signal
        s4['Touch'] = np.where(s4['RSI'] > c, -1, s4['Touch']) #short signal
        s4['Sustain'] = np.where(s4['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s4['Sustain'] = np.where(s4['Sustain'].shift(1) == 1, 1, 
                                   s4['Sustain']) 
        s4['Sustain'] = np.where(s4['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s4['Sustain'] = np.where(s4['Sustain'].shift(1) == 1, -1,
                                   s4['Sustain']) 
        s4['Sustain'] = np.where(s4['RSI'] > d, 0, s4['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s4['Sustain'] = np.where(s4['RSI'] < e, 0, s4['Sustain']) #never actually true when optimized
        s4['Regime'] = s4['Touch'] + s4['Sustain']
        s4['Strategy'] = (s4['Regime'][window:]).shift(1)*s4['LogRet'][window:]
        s4['Strategy'] = s4['Strategy'].fillna(0)
        endgains = 1
        endreturns = 1
        for g in s4['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s4['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        if endreturns > endgains:
            continue     
        if s4['Strategy'].std() == 0:
            continue
        sharpe = (s4['Strategy'].mean()-abs(s4['LogRet'].mean()))/s4['Strategy'].std()
        if sharpe < .035:
            continue
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        openseries = pd.Series(openspace)
        testset4winners[i] = openseries.values
        openspace[:] = []
    end4 = t.time()
    print('Datasets were tested in time 4, it took',end4-start4,'seconds')    
    Aggregate = pd.DataFrame()
    Aggregate = pd.concat([Aggregate, testset1winners, testset2winners,
                        testset3winners, testset4winners],axis = 1)
    Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
    return Aggregate
