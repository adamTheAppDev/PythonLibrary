# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:28:16 2017

@author: AmatVictoriaCuramIII
"""
import pandas as pd
import numpy as np
from YahooGrabber import YahooGrabber
ticker = '^GSPC'
s = YahooGrabber('UVXY')
window = 20
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
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
trim = (window * 2 - 1)
s = s[trim:]
replace = s[:trim]
s[['PDI','MDI','ADX','ADXmean']].plot(grid=True, figsize=(8,3))
s['Touch'] = np.where(s['DIdivergence'] > 0, 1,0) #long signal
s['Touch'] = np.where(s['DIdivergence'] < 0, -1, s['Touch']) #short signal
#s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
#s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
#                                 s['Sustain']) 
#s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
#s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
#                                 s['Sustain']) 
#s['Sustain'] = np.where(s['DIdivergence'] > -97.136948, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
#s['Sustain'] = np.where(s['DIdivergence'] < -34.577265, 0, s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] #+ s['Sustain']
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))