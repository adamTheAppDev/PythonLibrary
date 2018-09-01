
"""
Created on Thu Aug 31 08:55:46 2017
 -*- coding: utf-8 -*-
@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
empty = []
dataset = pd.DataFrame()
asone = pd.DataFrame()
start = t.time()
Ticker1 = YahooGrabber('^VIX') #we have these deltas
Ticker2 = YahooGrabber('UVXY') #we compute these deltas

conversionfactor = Ticker2['Adj Close'][-1]/Ticker1['Adj Close'][-1]
Ticker1delta = 1000
Ticker1cost = Ticker1['Adj Close'][-1]
#Ticker1cost = 18.3
Ticker1notional = Ticker1delta * Ticker1cost
#positioning
Ticker1position = .57
Ticker2position = .43
totalnotional = abs(Ticker1notional / Ticker1position)
Ticker2notional = totalnotional - abs(Ticker1notional)
Ticker2cost = Ticker2['Adj Close'][-1]
Ticker2delta = np.round((Ticker2notional / Ticker2cost), decimals = 2)
notionalcheck = str((Ticker2cost * Ticker2delta) / totalnotional)
print('If you have ' + str(Ticker1delta) + ' deltas in Ticker1, to reach ' +
            str(Ticker1position*100)  + " / " + str(Ticker2position*100) + " you must get " + str(Ticker2delta) +
            ' deltas in Ticker2 to rebalance.')
notionalvol = np.round((Ticker2position + float(notionalcheck)), decimals = 2)
print('The price deviation from the model suggests a tracking error of ' +
        str(((1-notionalvol))) + '%')
print('The total cost of the positions using shares will cost $' + 
            str(int(totalnotional)) +'.')
print('Ticker1 - $' + str(abs(Ticker1notional)))
print('Ticker2 - $' + str(Ticker2notional))