# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:36:25 2017

@author: AmatVictoriaCuramIII
"""

#This is a brute force optimization tool that is part of a kth fold optimization tool

import pandas as pd
from pandas_datareader import data
import numpy as np
import random as rand
def DefModADXStratOpt(ranger2, s):
#    s = data.DataReader(ticker, 'yahoo', start=starttime, end=endtime)
    empty = []
    counter = 0
    dataset = pd.DataFrame()
    for r in ranger2: 
        a = rand.randint(1,60)
        b = rand.random() * 2
        c = 100 - rand.random() * 200
        d = 100 - rand.random() * 200
        window = a
        s['AverageTrueRange'] = s['TrueRange'].rolling(window = window,
                                        center=False).sum()
        s['AverageTrueRange'] = ((s['AverageTrueRange'].shift(1)*(window-1
                                     ) + s['TrueRange']) / window)
        s['SmoothPDM'] = s['PDM'].rolling(window = window,
                                        center=False).sum()
        s['SmoothPDM'] = ((s['SmoothPDM'].shift(1)*(window-1
                                     ) + s['PDM']) / window)
        s['SmoothMDM'] = s['MDM'].rolling(window = window,
                                        center=False).sum()
        s['SmoothMDM'] = ((s['SmoothMDM'].shift(1)*(window-1
                                     ) + s['MDM']) / window)
        s['PDI'] = (100*(s['SmoothPDM']/s['AverageTrueRange']))
        s['MDI'] = (100*(s['SmoothMDM']/s['AverageTrueRange']))
        s['DIdiff'] = abs(s['PDI'] - s['MDI'])
        s['DIdivergence'] = s['PDI'] - s['MDI']
        s['DIsum'] = s['PDI'] + s['MDI']
        s['DX'] = (100 * (s['DIdiff']/s['DIsum']))
        s['DX'] = s['DX'].fillna(0)
        s['ADX'] = s['DX'].rolling(window = window, center = False).mean()
        s['ADXmean'] = s['ADX'].mean() * b
        s['Touch'] = np.where(s['DIdivergence'] < c, 1,0) #long signal
        s['Touch'] = np.where(s['DIdivergence'] > d, -1, s['Touch']) #short signal
        s['Sustain'] = 0
        s['Sustain'] = np.where(s['ADX'] >  s['ADXmean'], 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s['Sustain'] = np.where(s['ADX'] < s['ADXmean'], (s['Touch']*-1
                              ), s['Sustain']) #never actually true when optimized
        s['Regime'] = s['Touch'] + s['Sustain']
        s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
        s['Strategy'] = s['Strategy'].fillna(0)  
        if s['Strategy'].std() == 0:
            continue
        s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean(
                                                    ))/s['Strategy'].std()
        if s['sharpe'][-1] < -.05:        
            continue      
        empty.append(a)
        empty.append(b)
        empty.append(c)
        empty.append(d)
        empty.append(s['sharpe'][-1])
        emptyseries = pd.Series(empty)
        dataset[r] = emptyseries.values
        empty[:] = []      
    z1 = dataset.iloc[4]
    w1 = np.percentile(z1, 95)
    v1 = [] #this variable stores the Nth percentile of top performers
    DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
    for h in z1:
        if h > w1:
          v1.append(h)
    for j in v1:
          r = dataset.columns[(dataset == j).iloc[4]]    
          DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
    return DS1W
