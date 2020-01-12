# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:16:10 2016

@author: AmatVictoriaCuramIII
"""

#pandas_datareader is deprecated use YahooGrabber
#Information ratio is a summary statistic

import numpy as np
import pandas.io.data as web
from pandas_datareader import data
from pandas import read_csv
df = read_csv('companylist.csv', sep = ',')
symbols = df.Symbol.values
print(symbols)
port = symbols
bmk = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
bmk['LogRet'] = np.round(np.log(bmk['Close']/bmk['Close'].shift(1)), 3)
bmk['Mean'] = np.round((np.mean(bmk['LogRet'])), 5)*252
bmk['SD'] = np.std(bmk['LogRet'])*np.sqrt(252)
def InfoRat(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='9/1/2016')
    s['LogRet'] = (np.log(s['Close']/s['Close'].shift(1)))
    s['Mean'] = (np.mean(s['LogRet'])*252)
    s['SD'] = (np.std(s['LogRet'])*np.sqrt(252))
    s['InfoRat'] = (s['Mean'].tail(1)-bmk['Mean'].tail(1))/s['SD'].tail(1)
    print(s['InfoRat'].dropna())
for s in port:
    try:
        print(s, (InfoRat(s)))
    except OSError:
        pass
#    if int(s['InfoRat']) > 0:
#    elif int(s['InfoRat']) < 0:
#        print(s)
#press control-c to keyboard interrupt
