# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization tool

#Define function
def DefModADXAdviceGiver(Aggregate, q):
    #Import modules
    import numpy as np
    import pandas as pd
    #Assign variables
    base = 0
    size = len(Aggregate.iloc[0])    
    #Calculate ADX
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
    #Variable assignment
    advice = float()
    #For every param set
    for i in Aggregate: 
        #Assign params
        aa = Aggregate.loc[0,i] #numer of days for moving average window
        a = aa.astype(int)
        b = Aggregate[i].iloc[1]
        c = Aggregate[i].iloc[2] 
        d = Aggregate[i].iloc[3]
        window = a
        #Calculate ADX
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
        
        #Trim time series
#        trim = (window * 2 - 1)
#        q = q[trim:]
#        replace = q[:trim]
        #Directional methodology
        q['Touch'] = np.where(q['DIdivergence'] < c, 1,0) #long signal
        q['Touch'] = np.where(q['DIdivergence'] > d, -1, q['Touch']) #short signal
        q['Sustain'] = 0
        q['Sustain'] = np.where(q['ADX'] >  q['ADXmean'], 0, q['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        q['Sustain'] = np.where(q['ADX'] < q['ADXmean'], (q['Touch']*-1
                              ), q['Sustain']) #never actually true when optimized
        q['Regime'] = q['Touch'] + q['Sustain']
        #Apply position to returns
        q['Strategy'] = (q['Regime']).shift(1)*q['LogRet']
        q['Strategy'] = q['Strategy'].fillna(0)
        #Constraints
        if len(q) <= 1:
#            q = replace.append(q)
            continue
        #Directional assumption
        toadd = q['Regime'].iloc[-1]
        #Iteratively add to aggregate directional assumption stat
        base = base + toadd 
        #Directional assumption statistic 
        advice = base/size
#        q = replace.append(q)
#        print(base)
    #Output
    return advice
