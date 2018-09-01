# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""
#Get modules
from SAge import SAge
from SAverageReturn import SAverageReturn
from SCoeffVar import SCoeffVar
from STrend import STrend
from SGapDown import SGapDown
from DayOverAverageRollingVolume import DayOverAverageRollingVolume
from SAverageRollingVolume import SAverageRollingVolume
from SAdjustedClose import SAdjustedClose
from pandas import read_csv
from pandas_datareader import data
#Import and define info the list 
counter = 1
df = read_csv('companylist.csv', sep = ',')
df1 = df.set_index('Symbol')
symbols = df.Symbol.values
port = (symbols)
port1 = []
print(symbols)
for s in port:
    try:
        q = data.DataReader(s, 'yahoo', start='1/1/1950', end='01/01/2050')        
        if sum(SAdjustedClose(q)) > 5 and SAge(q) > 750 and sum(SGapDown(q)
        ) > .01 and sum(SAverageRollingVolume(q)
        ) > 500000 and sum(DayOverAverageRollingVolume(q)
        ) > 2 and sum(SAverageReturn(q)) < -.01 and sum(STrend(q)) < -0.01:
            print(s,  STrend(q), DayOverAverageRollingVolume(q), SAge(q))
            port1.append(s)
    except OSError:
        pass
    print(counter)
    counter = counter + 1
#List refined portfolio
print(port1)