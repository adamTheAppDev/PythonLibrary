# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an older version of a database scanning/query tool

#Import modules
from Age import Age
from AverageReturn import AverageReturn
from CoeffVar import CoeffVar
from Trend import Trend
from RelStrInd import RelStrInd
from pandas import read_csv

#Read in CSV with symbols
df = read_csv('bettersymbols.csv', sep = ',')
#Set index
df1 = df.set_index('Symbol')
#Variable assignment
symbols = df.Symbol.values
port = (symbols)
port1 = []
#Display all tickers
print(symbols)
#For all symbols to scan
for s in port:
    try:
        #Search params
        if Age(s) > 1000 and sum(AverageReturn(s)) < -.1 and sum(CoeffVar(s)) < -.5 and sum(
               Trend(s)) < -0.04 and sum(RelStrInd(s)) > 60:
            print(s, AverageReturn(s), Trend(s), CoeffVar(s), Age(s), RelStrInd(s))
            #Add to list
            port1.append(s)
    except OSError:
        pass
#List symbols that pass scan
print(port1)
