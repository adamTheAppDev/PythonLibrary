# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester, similar to incremental/martingale strategy
#Position size is based off technical information

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd

#Empty data strucures
tempdf = pd.DataFrame()
edgelist = []

#Assign ticker
ticker1 = 'UVXY'
#Variable assignment
lag = 15
atrwindow = 20
smawindow = 20
edgedays = 20
#Iterable
iterations = range(2,120)

#Request data
Asset1 = YahooGrabber(ticker1)

#Start timer
start = t.time()

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1)) 
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Alternative index
Asset1['idx'] = range(0,len(Asset1))
#Calculate simple moving average
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=smawindow, center=False).mean()

#Calculate ATR
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
#Horizontal line
Asset1['ZeroLine'] = 0
#Higher high than previous period
Asset1['Up'] = np.where(Asset1['High'] > Asset1['High'].shift(1), 1, 0)
#Position sizzing
Asset1['Position'] = Asset1['Up'].rolling(window = 10, center=False).sum()
Asset1['Position'] = Asset1['Position'].fillna(0)
Asset1['ModPosition'] = (Asset1['Position'] ** 2)/100
#Apply position to returns
Asset1['Strategy'] = -Asset1['ModPosition'] * Asset1['LogRet']
#Graphical display
Asset1[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
