# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:28:16 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester

#Import modules
import pandas as pd
import numpy as np
from YahooGrabber import YahooGrabber

#Input 
ticker = '^GSPC'

#Request data
s = YahooGrabber('UVXY')

#Variable assignmnet
window = 20

#Log return calculation
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#ATR calculation
s['Method1'] = s['High'] - s['Low']
s['Method2'] = abs((s['High'] - s['Adj Close'].shift(1)))
s['Method3'] = abs((s['Low'] - s['Adj Close'].shift(1)))
s['Method1'] = s['Method1'].fillna(0)
s['Method2'] = s['Method2'].fillna(0)
s['Method3'] = s['Method3'].fillna(0)
s['TrueRange'] = s[['Method1','Method2','Method3']].max(axis = 1)
s['AverageTrueRange'] = s['TrueRange'].rolling(window = window,
                                center=False).sum()
s['AverageTrueRange'] = ((s['AverageTrueRange'].shift(1)*(window-1
                             ) + s['TrueRange']) / window)

#ADX Calculation
s['PDM'] = (s['High'] - s['High'].shift(1))
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
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
s['ADXmean'] = s['ADX'].mean()

#Trimmer
trim = (window * 2 - 1)
s = s[trim:]
replace = s[:trim]

#Graphical display for indicator
s[['PDI','MDI','ADX','ADXmean']].plot(grid=True, figsize=(8,3))

#Strategy
s['Touch'] = np.where(s['DIdivergence'] > 0, 1,0) #long signal
s['Touch'] = np.where(s['DIdivergence'] < 0, -1, s['Touch']) #short signal
#Directional methodology
s['Regime'] = s['Touch']
#Strategy returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Performance metrics
s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()

#Display for strategy vs underlying
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
