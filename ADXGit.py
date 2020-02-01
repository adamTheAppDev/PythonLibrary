# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a techincal analysis tool

#Import modules
from pandas_datareader import data
import numpy as np

#Variable assignment
ticker = '^GSPC'
window = 14

#Request data - Use YahooGrabber
s = data.DataReader(ticker, 'yahoo', start='01/09/2010', end='01/01/2050')

#Return calculations
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#ATR calculations
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

#ADX calculations
s['PDM'] = (s['High'] - s['High'].shift(1)
s['MDM'] = (s['Low'].shift(1) - s['Low'])
s['PDM'] = s['PDM'][s['PDM'] > 0]
s['MDM'] = s['MDM'][s['MDM'] > 0]
s['PDM'] = s['PDM'].fillna(0)
s['MDM'] = s['MDM'].fillna(0)
            
#Smoothing by averages
s['SmoothPDM'] = s['PDM'].rolling(window = window,
                                center=False).sum()
s['SmoothPDM'] = ((s['SmoothPDM'].shift(1)*(window-1
                             ) + s['PDM']) / window)
s['SmoothMDM'] = s['MDM'].rolling(window = window,
                                center=False).sum()
s['SmoothMDM'] = ((s['SmoothMDM'].shift(1)*(window-1
                             ) + s['MDM']) / window)
      
#Normalize for volatility
s['PDI'] = (100*(s['SmoothPDM']/s['AverageTrueRange']))
s['MDI'] = (100*(s['SmoothMDM']/s['AverageTrueRange']))
s['DIdiff'] = abs(s['PDI'] - s['MDI'])
s['DIsum'] = s['PDI'] + s['MDI']
s['DX'] = (100 * (s['DIdiff']/s['DIsum']))
s['ADX'] = s['DX'].rolling(window = window, center = False).mean()
s['ADXmean'] = s['ADX'].mean()
trim = (window * 2 - 1)
            
#Trim for graphing
s = s[trim:]
#Graphical display
s[['PDI','MDI','ADX','ADXmean']].plot(grid=True, figsize=(8,3))
