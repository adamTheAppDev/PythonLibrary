# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""

#This is a scanning tool with technical analysis modules inside
#There is a more efficient way to do this process somewhere in the MasterLibrary

#Get modules to filter
from SAge import SAge
from SAverageReturn import SAverageReturn
from SCoeffVar import SCoeffVar
from STrend import STrend
from SGapDown import SGapDown
from DayOverAverageRollingVolume import DayOverAverageRollingVolume
from SAverageRollingVolume import SAverageRollingVolume
from SAdjustedClose import SAdjustedClose
from pandas import read_csv
from YahooGrabber import YahooGrabber

#Iteration counter
counter = 1

#Import stocks to filter 
df = read_csv('companylist.csv', sep = ',')
#Formatting
df1 = df.set_index('Symbol')
symbols = df.Symbol.values
#Define portfolio of stocks to scan
port = (symbols)
#End portfolio of stocks that pass scan
port1 = []
print(symbols)
#For all tickers to be scanned
for s in port:
    try:
        #Data req is faster from local storage than HTML parse
        q = YahooGrabber(s)
        #If passes scan
        if sum(SAdjustedClose(q)) > 5 and SAge(q) > 750 and sum(SGapDown(q)
        ) > .01 and sum(SAverageRollingVolume(q)
        ) > 500000 and sum(DayOverAverageRollingVolume(q)
        ) > 2 and sum(SAverageReturn(q)) < -.01 and sum(STrend(q)) < -0.01:
            print(s,  STrend(q), DayOverAverageRollingVolume(q), SAge(q))
            #Add to final list
            port1.append(s)
    except OSError:
        pass
    print(counter)
    counter = counter + 1
#List refined portfolio
print(port1)
