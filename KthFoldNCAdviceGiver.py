# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool

#Define function
def DefNCAdviceGiver(Aggregate, q):
    #Import modules
    import numpy as np
    import pandas as pd
    #Read in data
    Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
    #Remove duplicate columns
    Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
    #Zeros
    base = 0
    advice = 0
    #Read in params
    size = len(Aggregate.iloc[0])    
    #Calculate ADI
    q['CLV'] = (((q['Adj Close'] - q['Low']) - (q['High'] - q['Adj Close']))
                        / (q['High'] - q['Low']))
    q['ADI'] = (q['Volume'] * q['CLV']).cumsum()
    values = q['ADI']
    #Calculate log returns
    q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
    q['LogRet'] = q['LogRet'].fillna(0) #change to s if after 6pm 
    #For all params sets
    for i in Aggregate:
        #Read in params
        aa = Aggregate.loc[0,i] #numer of days for moving average window
        a = aa.astype(int)
        bb = Aggregate.loc[1,i] #numer of days for moving average window
        b = bb.astype(int)
        cc = Aggregate.loc[2,i] #numer of days for volume window
        c = cc.astype(int)
        d = Aggregate[i].iloc[3] 
        e = Aggregate[i].iloc[4]
        f = Aggregate[i].iloc[5]
        g = Aggregate[i].iloc[6]
        #Assign weights for EMA calculation
        weights = np.repeat(1.0, a)/a
        weights2 = np.repeat(1.0, b)/b
        #EMAs
        smas = np.convolve(values, weights, 'valid')
        smas2 = np.convolve(values, weights2, 'valid')
        #Time series trimmer
        trim = len(smas) - len(smas2)
        smas = smas[trim:]
        totaltrim = len(weights2)
        replace = q[:totaltrim]
        q = q[totaltrim:]
        #More time series trimming
        clipper = len(smas) -len(q)
        clipper2 = len(smas2) - len(q)
        q.loc[:,'ADIEMAsmall'] = smas[clipper:]
        q.loc[:,'ADIEMAlarge'] = smas2[clipper2:]
        q = replace.append(q)
        #Param assignment
        volumewindow = c
        #Average rolling volume calculation
        q.loc[:,'AverageRollingVolume'] = q['Volume'].rolling(center=False,
                                            window=volumewindow).mean()
        #Normalized chaikin calculation
        q.loc[:,'Chaikin'] = q['ADIEMAsmall'] - q['ADIEMAlarge']
        q.loc[:,'NormChaikin'] = q['Chaikin']/q['AverageRollingVolume']
        #Trim time series 
        kk = q[:volumewindow-1]        
        q = q[volumewindow-1:] 
        #Directional methodology
        q.loc[:,'Touch'] = np.where(q['NormChaikin'] < d, 1,0) #long signal
        q.loc[:,'Touch'] = np.where(q['NormChaikin'] > e, -1, q['Touch']) #short signal
        q.loc[:,'Sustain'] = np.where(q['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        q.loc[:,'Sustain'] = np.where(q['Sustain'].shift(1) == 1, 1, 
                                         q['Sustain']) 
        q.loc[:,'Sustain'] = np.where(q['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        q.loc[:,'Sustain'] = np.where(q['Sustain'].shift(1) == -1, -1,
                                         q['Sustain']) 
        q.loc[:,'Sustain'] = np.where(q['NormChaikin'] > f, 0, q['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        q.loc[:,'Sustain'] = np.where(q['NormChaikin'] < g, 0, q['Sustain']) #never actually true when optimized
        q.loc[:,'Regime'] = q['Touch'] + q['Sustain']
        #Constraint
        if len(q) <= 1:
            continue
        #Add to directional statistic    
        toadd = q['Regime'].iloc[-1]
        #Total directional assumptions from params
        base = base + toadd 
        #Recalculate aggregate directional statistic
        advice = base/size
        #Add to list
        q = kk.append(q)
    #Output aggregate directional statistic
    return advice
