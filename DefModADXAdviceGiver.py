# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 23:20:32 2017

@author: AmatVictoriaCuramIII
"""

def DefModADXAdviceGiver(Aggregate, q):
    import numpy as np
    import pandas as pd
    base = 0
    size = len(Aggregate.iloc[0])    
    q['UpMove'] = q['High'] - q['High'].shift(1)
    q['DownMove'] = q['Low'] - q['Low'].shift(1)
    q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
    q['LogRet'] = q['LogRet'].fillna(0)
    q['Method1'] = q['High'] - q['Low']
    q['Method2'] = abs((q['High'] - q['Adj Close'].shift(1)))
    q['Method3'] = abs((q['Low'] - q['Adj Close'].shift(1)))
    q['Method1'] = q['Method1'].fillna(0)
    q['Method2'] = q['Method2'].fillna(0)
    q['Method3'] = q['Method3'].fillna(0)
    q['TrueRange'] = q[['Method1','Method2','Method3']].max(axis = 1)
    q['PDM'] = (q['High'] - q['High'].shift(1))
    q['MDM'] = (q['Low'].shift(1) - q['Low'])
    q['PDM'] = q['PDM'][q['PDM'] > 0]
    q['MDM'] = q['MDM'][q['MDM'] > 0]
    q['PDM'] = q['PDM'].fillna(0)
    q['MDM'] = q['MDM'].fillna(0)
    advice = float()
    for i in Aggregate:             
        aa = Aggregate.loc[0,i] #numer of days for moving average window
        a = aa.astype(int)
        b = Aggregate[i].iloc[1]
        c = Aggregate[i].iloc[2] 
        d = Aggregate[i].iloc[3]
        window = a
        q['AverageTrueRange'] = q['TrueRange'].rolling(window = window,
                                        center=False).sum()
        q['AverageTrueRange'] = ((q['AverageTrueRange'].shift(1)*(window-1
                                     ) + q['TrueRange']) / window)
        q['SmoothPDM'] = q['PDM'].rolling(window = window,
                                        center=False).sum()
        q['SmoothPDM'] = ((q['SmoothPDM'].shift(1)*(window-1
                                     ) + q['PDM']) / window)
        q['SmoothMDM'] = q['MDM'].rolling(window = window,
                                        center=False).sum()
        q['SmoothMDM'] = ((q['SmoothMDM'].shift(1)*(window-1
                                     ) + q['MDM']) / window)
        q['PDI'] = (100*(q['SmoothPDM']/q['AverageTrueRange']))
        q['MDI'] = (100*(q['SmoothMDM']/q['AverageTrueRange']))
        q['DIdiff'] = abs(q['PDI'] - q['MDI'])
        q['DIdivergence'] = q['PDI'] - q['MDI']
        q['DIsum'] = q['PDI'] + q['MDI']
        q['DX'] = (100 * (q['DIdiff']/q['DIsum']))
        q['DX'] = q['DX'].fillna(0)
        q['ADX'] = q['DX'].rolling(window = window, center = False).mean()
        q['ADXmean'] = q['ADX'].mean() * b
#        trim = (window * 2 - 1)
#        q = q[trim:]
#        replace = q[:trim]
        q['Touch'] = np.where(q['DIdivergence'] < c, 1,0) #long signal
        q['Touch'] = np.where(q['DIdivergence'] > d, -1, q['Touch']) #short signal
        q['Sustain'] = 0
        q['Sustain'] = np.where(q['ADX'] >  q['ADXmean'], 0, q['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        q['Sustain'] = np.where(q['ADX'] < q['ADXmean'], (q['Touch']*-1
                              ), q['Sustain']) #never actually true when optimized
        q['Regime'] = q['Touch'] + q['Sustain']
        q['Strategy'] = (q['Regime']).shift(1)*q['LogRet']
        q['Strategy'] = q['Strategy'].fillna(0)
        if len(q) <= 1:
#            q = replace.append(q)
            continue
        toadd = q['Regime'].iloc[-1]
        base = base + toadd 
        advice = base/size
#        q = replace.append(q)
#        print(base)
    return advice