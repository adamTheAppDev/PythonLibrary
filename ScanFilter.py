# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 23:29:44 2017

@author: AmatVictoriaCuramIII
"""
#Get modules
from Age import Age
from AverageReturn import AverageReturn
from CoeffVar import CoeffVar
from Trend import Trend
from RelStrInd import RelStrInd
from pandas import read_csv
#Import and define info the list 
df = read_csv('bettersymbols.csv', sep = ',')
df1 = df.set_index('Symbol')
symbols = df.Symbol.values
port = (symbols)
port1 = []
print(symbols)
for s in port:
    try:
        if Age(s) > 1000 and sum(AverageReturn(s)) < -.1 and sum(CoeffVar(s)) < -.5 and sum(
               Trend(s)) < -0.04 and sum(RelStrInd(s)) > 60:
            print(s, AverageReturn(s), Trend(s), CoeffVar(s), Age(s), RelStrInd(s))
            port1.append(s)
    except OSError:
        pass
#List refined portfolio
print(port1)