# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""

#This lists all stock tickers that pass the scan

#Get modules

from DatabaseGrabber import DatabaseGrabber
import os
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import pandas as pd
import numpy as np
import math
#Got to get that payback!!
Counter = 0
Empty = []
Empty2 = []
Universe = os.listdir('F:\\Users\\AmatVictoriaCuram\\FDL\\DataSources\\YahooSource\\ProcessedData\\DAY')
UniverseTickers = [s[4:] for s in Universe]
#print(symbols)
for Ticker in UniverseTickers[:150]:
    try:
        Asset = YahooSourceDailyGrabber(Ticker)    
#Price filter
        if Asset['Adj Close'][-1] < 10:
            continue
        if Asset['Adj Close'][-1] > 90:
            continue
#Volume filter
        if Asset['1wkRollingAverageVolume'][-1] < 1000000:
            continue
        DY = Asset['DividendYield'][-1]
        if math.isnan(DY) == True:
            continue
        if DY < .015:
            continue
        Empty.append(Ticker)
        Empty2.append(DY)
        Emptyseries = pd.Series(Empty)
        print(DY)
        print(Ticker)
        

    except OSError:
        pass
#List refined portfolio
RefinedPortfolio = pd.DataFrame(data = Empty2, index=Empty, columns = ['Dividend'])
SortedPortfolio = RefinedPortfolio.sort_values(by = ['Dividend'], ascending = True)
SortedPortfolio = SortedPortfolio.dropna()
print(SortedPortfolio)