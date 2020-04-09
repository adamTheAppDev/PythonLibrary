# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#this is part of a kth fold optimization tool with RSI indicator

#Import modules
import numpy as np
#Define function
def RSIaggregate(s, Aggregate):
    #Delete duplicate columns
    Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
    #Zeros
    base = 0
    #Read in params
    size = len(Aggregate.iloc[0])
    #For all param sets 
    for i in Aggregate:
        #Read in params
        a = Aggregate[i].iloc[0]
        aa = a.astype(int)
        b = Aggregate[i].iloc[1]
        c = Aggregate[i].iloc[2]
        d = Aggregate[i].iloc[3]
        e = Aggregate[i].iloc[4]
        #Calculate log returns
        s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
        s['LogRet'] = s['LogRet'].fillna(0)
        close = s['Adj Close']
        #Assign params
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
        s['RSI'] = RSI
        s['RSI'] = s['RSI'].fillna(0)
        #Directional assumption
        s['Touch'] = np.where(s['RSI'] < b, 1,0) #long signal
        s['Touch'] = np.where(s['RSI'] > c, -1, s['Touch']) #short signal
        s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                  s['Sustain']) 
        s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                s['Sustain']) 
        s['Sustain'] = np.where(s['RSI'] > d, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s['Sustain'] = np.where(s['RSI'] < e, 0, s['Sustain']) #never actually true when optimized
        s['Regime'] = s['Touch'] + s['Sustain']
        #Directional assumption
        toadd = s['Regime'][-1]
        #Add to aggregate directional assumption
        base = base + toadd 
        #Total aggregate directional assumption
        advice = base/size
    #Output aggregate directional assumption
    return advice  
