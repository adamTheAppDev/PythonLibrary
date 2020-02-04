# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a portfolio analysis tool, useful for pair trades and hedging

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Assign variables
Empty = []
Dataset = pd.DataFrame()
start = t.time()

#Request data
Ticker1 = YahooGrabber('^VIX') #we have these deltas
Ticker2 = YahooGrabber('UVXY') #we compute these deltas

#Spot price ratios
ConversionFactor = Ticker2['Adj Close'][-1]/Ticker1['Adj Close'][-1]

#Number of deltas/shares in ticker 1
Ticker1Delta = 1000
#Spot price ticker 1
Ticker1Cost = Ticker1['Adj Close'][-1]
#Total position value
Ticker1Notional = Ticker1Delta * Ticker1Cost
#Portfolio allocation
Ticker1Position = .57
Ticker2Position = .43

#Desired value of portfolio 
TotalNotional = abs(Ticker1Notional / Ticker1Position)

#Decuding position in ticker 2
Ticker2Notional = TotalNotional - abs(Ticker1Notional)
Ticker2Cost = Ticker2['Adj Close'][-1]
Ticker2Delta = np.round((Ticker2Notional / Ticker2Cost), decimals = 2)

#Confirming
NotionalCheck = str((Ticker2Cost * Ticker2Delta) / TotalNotional)

print('If you have ' + str(Ticker1Delta) + ' deltas in Ticker1, to reach ' +
            str(Ticker1Position*100)  + " / " + str(Ticker2Position*100) + " you must get " + str(Ticker2Delta) +
            ' deltas in Ticker2 to rebalance.')
NotionalVol = np.round((Ticker2Position + float(NotionalCheck)), decimals = 2)
print('The price deviation from the model suggests a tracking error of ' +
        str(((1-NotionalVol))) + '%')
print('The total cost of the positions using shares will cost $' + 
            str(int(TotalNotional)) +'.')
print('Ticker1 - $' + str(abs(Ticker1Notional)))
print('Ticker2 - $' + str(Ticker2Notional))
