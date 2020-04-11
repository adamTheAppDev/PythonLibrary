# -*- coding: utf-8 -*-

"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import pandas as pd
from pandas_datareader import data
import numpy as np
#Assign ticker
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='01/01/2010', end='01/01/2050')
#Param assignment
window = 3
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Calculate ATR
s['UpMove'] = s['High'] - s['High'].shift(1)
s['DownMove'] = s['Low'] - s['Low'].shift(1)
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
#Calculate ADX
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
s['ADXmean'] = s['ADX'].mean() * 1.06907
#Indicator graphical display
s[['PDI','MDI','ADX','ADXmean']].plot(grid=True, figsize=(8,3))
#Directional methodology
s['Touch'] = np.where(s['DIdivergence'] < 20.1964, 1,0) #long signal
s['Touch'] = np.where(s['DIdivergence'] > 25.183, -1, s['Touch']) #short signal
s['Sustain'] = 0 
s['Sustain'] = np.where(s['ADX'] >  s['ADXmean'], 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['ADX'] < s['ADXmean'], (s['Touch']*-1), s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] + s['Sustain']
#apply position to returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#Performance metric
s['sharpe'] = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
#Graphical display
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
#Add data back
s = replace.append(s)
