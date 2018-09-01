# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:41:57 2017

@author: AmatVictoriaCuramIII
"""
def DefNCAdviceGiver(Aggregate, q):
    import numpy as np
    import pandas as pd
    Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
    Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
    base = 0
    size = len(Aggregate.iloc[0])    
    q['CLV'] = (((q['Adj Close'] - q['Low']) - (q['High'] - q['Adj Close']))
                        / (q['High'] - q['Low']))
    q['ADI'] = (q['Volume'] * q['CLV']).cumsum()
    values = q['ADI']
    q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
    q['LogRet'] = q['LogRet'].fillna(0) #change to s if after 6pm 
    advice = 0
    for i in Aggregate:
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
        weights = np.repeat(1.0, a)/a
        weights2 = np.repeat(1.0, b)/b
        smas = np.convolve(values, weights, 'valid')
        smas2 = np.convolve(values, weights2, 'valid')
        trim = len(smas) - len(smas2)
        smas = smas[trim:]
        totaltrim = len(weights2)
        replace = q[:totaltrim]
        q = q[totaltrim:]
        clipper = len(smas) -len(q)
        clipper2 = len(smas2) - len(q)
        q.loc[:,'ADIEMAsmall'] = smas[clipper:]
        q.loc[:,'ADIEMAlarge'] = smas2[clipper2:]
        q = replace.append(q)
        volumewindow = c
        q.loc[:,'AverageRollingVolume'] = q['Volume'].rolling(center=False,
                                            window=volumewindow).mean()
        q.loc[:,'Chaikin'] = q['ADIEMAsmall'] - q['ADIEMAlarge']
        q.loc[:,'NormChaikin'] = q['Chaikin']/q['AverageRollingVolume']
        kk = q[:volumewindow-1]        
        q = q[volumewindow-1:]        
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
        if len(q) <= 1:
            continue
        toadd = q['Regime'].iloc[-1]
        base = base + toadd 
        advice = base/size
        q = kk.append(q)
    return advice