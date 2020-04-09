# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is the middle part of a kth fold optimization tool
#Its definitely written out the long way
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
#from pandas_datareader import data
import numpy as np
import pandas as pd
import time as t

#Define function
def RelStrIndTester(s1, s2, s3, s4, testset1, testset2, testset3, testset4):
    
    #Structures for param sets
    testset1winners = pd.DataFrame()
    testset2winners = pd.DataFrame()
    testset3winners = pd.DataFrame()
    testset4winners = pd.DataFrame()   
    #Ignore error text
    np.seterr(divide='ignore', invalid='ignore')
    #Start timer
    start1 = t.time()
    #Delete duplicate columns in testsets
    testset1 = testset1.loc[:,~testset1.columns.duplicated()]
    testset2 = testset2.loc[:,~testset2.columns.duplicated()]
    testset3 = testset3.loc[:,~testset3.columns.duplicated()]
    testset4 = testset4.loc[:,~testset4.columns.duplicated()]
    #For params in testset
    for i in testset1:
        #Read in params
        a = testset1[i].iloc[0]
        aa = a.astype(int)
        b = testset1[i].iloc[1]
        c = testset1[i].iloc[2]
        d = testset1[i].iloc[3]
        e = testset1[i].iloc[4]
        #Empty data structures
        openspace = []
        openseries = pd.Series()
        #Calculate log returns
        s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1)) 
        s1['LogRet'] = s1['LogRet'].fillna(0)
        close = s1['Adj Close']
        #Param assignment
        window = aa
        #Calculate RSI
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
        #Directional methodology
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
        #Apply position to returns
        s1['Strategy'] = (s1['Regime'][window:]).shift(1)*s1['LogRet'][window:]
        s1['Strategy'] = s1['Strategy'].fillna(0)
        #Compound returns
        endgains = 1
        endreturns = 1
        for g in s1['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s1['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        #Constraints
        if endreturns > endgains:
            continue       
        if s1['Strategy'].std() == 0:
            continue
        sharpe = (s1['Strategy'].mean()-abs(s1['LogRet'].mean()))/s1['Strategy'].std()
        #Constraints
        if sharpe < .035:
            continue
        #Save params to list
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        #List to series
        openseries = pd.Series(openspace)
        #Series to dataframe
        testset1winners[i] = openseries.values
        #Clear list
        openspace[:] = []
    #End timer
    end1 = t.time()
    #Timer stats
    print('Datasets were tested in time 1, it took',end1-start1,'seconds')
    
    #Start timer
    start2 = t.time()
    #For params in testset
    for i in testset2:
        #Read in params
        a = testset2[i].iloc[0]
        aa = a.astype(int)
        b = testset2[i].iloc[1]
        c = testset2[i].iloc[2]
        d = testset2[i].iloc[3]
        e = testset2[i].iloc[4]
        #Empty data structures
        openspace = []
        openseries = pd.Series()
        #Calculate log returns
        s2['LogRet'] = np.log(s2['Adj Close']/s2['Adj Close'].shift(1)) 
        s2['LogRet'] = s2['LogRet'].fillna(0)
        close = s2['Adj Close']
        #Param assignment
        window = aa  
        #Calculate RSI
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
        #Directional methodology
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
        #Apply position to returns
        s2['Strategy'] = (s2['Regime'][window:]).shift(1)*s2['LogRet'][window:]
        s2['Strategy'] = s2['Strategy'].fillna(0)
        #Compound returns
        endgains = 1
        endreturns = 1
        for g in s2['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s2['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        #Constraints
        if endreturns > endgains:
            continue  
        if s2['Strategy'].std() == 0:
            continue
        sharpe = (s2['Strategy'].mean()-abs(s2['LogRet'].mean()))/s2['Strategy'].std()
        #Constraints
        if sharpe < .035:
            continue
        #Save params to list
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        #List to series
        openseries = pd.Series(openspace)
        #Series to dataframe
        testset2winners[i] = openseries.values
        #Clear list
        openspace[:] = []
    #End timer
    end2 = t.time()
    #Timer stats
    print('Datasets were tested in time 2, it took',end2-start2,'seconds')
    
    #Start timer
    start3 = t.time()
    #For params in testset
    for i in testset3:
        #Read in params
        a = testset3[i].iloc[0]
        aa = a.astype(int)
        b = testset3[i].iloc[1]
        c = testset3[i].iloc[2]
        d = testset3[i].iloc[3]
        e = testset3[i].iloc[4]
        #Empty data structures
        openspace = []
        openseries = pd.Series()
        #Calculate log returns
        s3['LogRet'] = np.log(s3['Adj Close']/s3['Adj Close'].shift(1)) 
        s3['LogRet'] = s3['LogRet'].fillna(0)
        close = s3['Adj Close']
        #Param assignment
        window = aa  
        #Calculate RSI
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
        #Directional methodology
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
        #Apply position to returns
        s3['Strategy'] = (s3['Regime'][window:]).shift(1)*s3['LogRet'][window:]
        s3['Strategy'] = s3['Strategy'].fillna(0)
        #Compound returns
        endgains = 1
        endreturns = 1
        for g in s3['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s3['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        #Constraints
        if endreturns > endgains:
            continue     
        if s3['Strategy'].std() == 0:
            continue
        sharpe = (s3['Strategy'].mean()-abs(s3['LogRet'].mean()))/s3['Strategy'].std()
        #Constraints
        if sharpe < .035:
            continue
        #Save params to list
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        #List to series
        openseries = pd.Series(openspace)
        #Series to dataframe
        testset3winners[i] = openseries.values
        #Clear list
        openspace[:] = []
    #End timer
    end3 = t.time()
    #Timer stats
    print('Datasets were tested in time 3, it took',end3-start3,'seconds')    
    
    #Start timer
    start4 = t.time()    
    #For params in testset
    for i in testset4:
        #Read in params
        a = testset4[i].iloc[0]
        aa = a.astype(int)
        b = testset4[i].iloc[1]
        c = testset4[i].iloc[2]
        d = testset4[i].iloc[3]
        e = testset4[i].iloc[4]
        #Empty data structures
        openspace = []
        openseries = pd.Series()
        #Calculate log returns
        s4['LogRet'] = np.log(s4['Adj Close']/s4['Adj Close'].shift(1)) 
        s4['LogRet'] = s4['LogRet'].fillna(0)
        close = s4['Adj Close']
        #Param assignment
        window = aa  
        #Calculate RSI
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
        #Directional methodology
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
        #Apply position to returns
        s4['Strategy'] = (s4['Regime'][window:]).shift(1)*s4['LogRet'][window:]
        s4['Strategy'] = s4['Strategy'].fillna(0)
        #Compound returns
        endgains = 1
        endreturns = 1
        for g in s4['LogRet']:
            slate = endreturns * (1+g)
            endreturns = slate
        for q in s4['Strategy']:
            otherslate = endgains * (1+q)
            endgains = otherslate
        #Constraints
        if endreturns > endgains:
            continue     
        if s4['Strategy'].std() == 0:
            continue
        sharpe = (s4['Strategy'].mean()-abs(s4['LogRet'].mean()))/s4['Strategy'].std()
        #Constraints
        if sharpe < .035:
            continue
        #Save params to list
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(endreturns)
        openspace.append(endgains)
        openspace.append(sharpe)
        #List to series
        openseries = pd.Series(openspace)
        #Series to dataframe
        testset4winners[i] = openseries.values
        #Clear list
        openspace[:] = []
    #End timer
    end4 = t.time()
    #Timer stats
    print('Datasets were tested in time 4, it took',end4-start4,'seconds')    
    #Empty structure
    Aggregate = pd.DataFrame()
    #Assign all top params to aggregate param set
    Aggregate = pd.concat([Aggregate, testset1winners, testset2winners,
                        testset3winners, testset4winners],axis = 1)
    #Delete duplicate columns 
    Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
    #Output aggregate param set
    return Aggregate
