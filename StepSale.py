# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 08:34:43 2018

@author: AmatVictoriaCuramIII
"""

#StepSale Strategy

from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd


tempdf = pd.DataFrame()
edgelist = []
ticker1 = 'UVXY'
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
iterations = range(2,120)
Asset1 = YahooGrabber(ticker1)
start = t.time()

Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['idx'] = range(0,len(Asset1))
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=smawindow, center=False).mean()

Asset1['UpMove'] = Asset1['High'] - Asset1['High'].shift(1)
Asset1['DownMove'] = Asset1['Low'] - Asset1['Low'].shift(1)
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['Method1'] = Asset1['High'] - Asset1['Low']
Asset1['Method2'] = abs((Asset1['High'] - Asset1['Close'].shift(1)))
Asset1['Method3'] = abs((Asset1['Low'] - Asset1['Close'].shift(1)))
Asset1['Method1'] = Asset1['Method1'].fillna(0)
Asset1['Method2'] = Asset1['Method2'].fillna(0)
Asset1['Method3'] = Asset1['Method3'].fillna(0)
Asset1['TrueRange'] = Asset1[['Method1','Method2','Method3']].max(axis = 1)

#ATR in points not %

Asset1['AverageTrueRangePoints'] = Asset1['TrueRange'].rolling(window = atrwindow,
                                center=False).mean()

Asset1['ZeroLine'] = 0

Asset1['Up'] = np.where(Asset1['High'] > Asset1['High'].shift(1), 1, 0)
Asset1['Position'] = Asset1['Up'].rolling(window = 10, center=False).sum()
Asset1['Position'] = Asset1['Position'].fillna(0)
Asset1['ModPosition'] = (Asset1['Position'] ** 2)/100
Asset1['Strategy'] = -Asset1['ModPosition'] * Asset1['LogRet']
Asset1[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))