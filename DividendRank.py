# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a directory scanning and sorting tool
#Lists and sorts all stock tickers that pass the scan

#Import modules
from DatabaseGrabber import DatabaseGrabber
import os
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
import pandas as pd
import numpy as np
import math

#Variable assignment
Counter = 0
Empty = []
Empty2 = []

#Assign tickers in universe 
Universe = os.listdir('F:\\Users\\Username\\DirectoryLocation\\DataSources\\YahooSource\\ProcessedData\\DAY')
UniverseTickers = [s[4:] for s in Universe]
#print(symbols)

#For all tickers in universe
for Ticker in UniverseTickers[:150]:
    try:
        #Request data
        Asset = YahooSourceDailyGrabber(Ticker)    
        #Price filter
        if Asset['Adj Close'][-1] < 10:
            continue
        if Asset['Adj Close'][-1] > 90:
            continue
        #Volume filter
        if Asset['1wkRollingAverageVolume'][-1] < 1000000:
            continue
        #Dividend yield based on last price
        DY = Asset['DividendYield'][-1]
        #No dividend - constraint
        if math.isnan(DY) == True:
            continue
        #Dividend value constraint
        if DY < .015:
            continue
        #If passes scan, then add to lists for later
        Empty.append(Ticker)
        Empty2.append(DY)
        #List to Series
        Emptyseries = pd.Series(Empty)
        #Print ticker + yield
        print(DY)
        print(Ticker)
        
    #If ticker is not available in database, pass
    except OSError:
        pass
    
#List refined portfolio
RefinedPortfolio = pd.DataFrame(data = Empty2, index=Empty, columns = ['Dividend'])
#Sort dividends by value
SortedPortfolio = RefinedPortfolio.sort_values(by = ['Dividend'], ascending = True)
#Clean data
SortedPortfolio = SortedPortfolio.dropna()
#Display
print(SortedPortfolio)
