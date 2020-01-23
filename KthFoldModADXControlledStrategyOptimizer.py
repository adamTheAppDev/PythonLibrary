# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 01:24:05 2017

@author: AmatVictoriaCuramIII
"""

#This is a brute force optimization tool that is part of a kth fold optimization tool

def DefModADXControlledStrategyOptimizer(ranger2, s):
    import numpy as np
    import pandas as pd
    import random as rand
    empty = []
    winners = pd.DataFrame()
    for r in ranger: 
        a = rand.randint(2,15)
        b = rand.randint(2,15)
        c = rand.random() * 3
        d = rand.random() * 3
        e = rand.random() * 3
        f = rand.random() * 3
        
        s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
        s['LogRet'] = s['LogRet'].fillna(0)
        s['Regime'] = np.where(s['Advice'] > -1.874201, 1, 0)
        s['Regime'] = np.where(s['Advice'] < -.328022, -1, s['Regime'])
        s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
        s['Strategy'] = s['Strategy'].fillna(0)
        s['NewStrategy'] = s['Strategy']
        s['Width'] = (s['High'] - s['Low'])/s['Open'] 
        s['OverNight'] = (s['Open'] - s['Adj Close'].shift(1))/s['Adj Close'].shift(1)
        s['RollingWidth'] = s['Width'].rolling(center = False, window=a).mean()
        s['RollingOverNight'] = abs(s['OverNight']).rolling(center=False, window=b).mean()
        s['DayUp'] = (s['High'] - s['Adj Close'].shift(1))/s['Open']
        s['DayUp'] = s['DayUp'][s['DayUp']> 0]
        s['DayUp'] = s['DayUp'].fillna(0)
        s['DayDown'] = (s['Adj Close'].shift(1) - s['Low'])/s['Open']
        s['DayDown'] = s['DayDown'][s['DayDown']> 0]
        s['DayDown'] = s['DayDown'].fillna(0)
        s['sharpe'] = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
        s['LongGains'] = np.where(s['DayUp'] >= (s['RollingWidth']/c),s['RollingWidth']/c,0)
        s['ShortGains'] = np.where(s['DayDown'] >= (s['RollingWidth']/d),s['RollingWidth']/d,0)
        s['LongStop'] = np.where(s['OverNight'] <= (s['RollingWidth'].shift(1)/e * -1),
                                                        s['OverNight'] ,0)
        s['ShortStop'] = np.where(s['OverNight'] >= s['RollingWidth'].shift(1)/f,
                                                        (s['OverNight']*-1) ,0)
        s['NewStrategy'] = np.where(s['Regime'].shift(1) == 1,s['LongGains'],0)
        s['NewStrategy'] = np.where(s['Regime'].shift(1) == -1,s['ShortGains'],s['NewStrategy'])
        s['NewStrategy'] = np.where(s['NewStrategy'] == 0, s['Strategy'], s['NewStrategy'])
        s['NewStrategy'] = np.where(s['LongStop'] < 0, s['LongStop'], s['NewStrategy'])
        s['NewStrategy'] = np.where(s['ShortStop'] < 0, s['ShortStop'], s['NewStrategy'])
        s['newsharpe'] = (s['NewStrategy'].mean()-abs(s['LogRet'].mean()))/s['NewStrategy'].std()  
        if s['newsharpe'][-1] < -400:
            continue
        empty.append(a)
        empty.append(b)
        empty.append(c)
        empty.append(d)
        empty.append(e)
        empty.append(f)
        empty.append(s['sharpe'][-1])
        empty.append(s['newsharpe'][-1])    
        emptyseries = pd.Series(empty)
        winners[r] = emptyseries.values
        empty[:] = []      
    z = winners.iloc[7]
    w = np.percentile(z, 80)
    v = [] #this variable stores the Nth percentile of top performers
    DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
    for h in z:
        if h > w:
          v.append(h)
    for j in v:
          r = winners.columns[(winners == j).iloc[7]]    
          DS1W = pd.concat([DS1W,winners[r]], axis = 1)
    y = max(z)
    x = winners.columns[(winners == y).iloc[7]] #this is the column number
    return winners[x] #this is the dataframe index based on column number
        
