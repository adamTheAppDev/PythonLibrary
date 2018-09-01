# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 23:53:08 2017

@author: AmatVictoriaCuramIII
"""
#somehow, we will recreate VXV, then we will recreate UVXY somehow..
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

Empty = []
Match = pd.DataFrame()
Portfolio = pd.DataFrame()

Ticker1 = 'UVXY'
Ticker2 = '^VXV'
Ticker3 = '^VIX'

Asset1 = DatabaseGrabber(Ticker1)
Asset2 = DatabaseGrabber(Ticker2)
Asset3 = DatabaseGrabber(Ticker3)

Match['UVXY'] = Asset1['Adj Close']
Match['^VXV'] = Asset2['Adj Close'][-len(Asset1):]
Match['^VIX'] = Asset3['Adj Close'][-len(Asset1):]

#uh, you have to cointegrate. Regress VIX price in meaningful sections against time and then use beta as theta decay -- and subtract (beta * # day of period) from spot vix = stationary-arity-y VIX