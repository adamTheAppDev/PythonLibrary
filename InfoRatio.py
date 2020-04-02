# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""


#pandas_datareader is deprecated use YahooGrabber
#Information ratio is a summary statistic

#Import modules
import numpy as np
import pandas.io.data as web
from pandas_datareader import data
from pandas import read_csv

#Read in data
df = read_csv('companylist.csv', sep = ',')
#Assign variable
symbols = df.Symbol.values
print(symbols)

#Request data
bmk = data.DataReader('^GSPC', 'yahoo', start='1/1/1900', end='01/01/2050')
#Calculate log returns
bmk['LogRet'] = np.round(np.log(bmk['Close']/bmk['Close'].shift(1)), 3)
#Time series statistics
bmk['Mean'] = np.round((np.mean(bmk['LogRet'])), 5)*252
bmk['SD'] = np.std(bmk['LogRet'])*np.sqrt(252)
#Define function
def InfoRat(s):
    #Request data
    s = web.get_data_yahoo(s, start='1/1/1900', end='9/1/2016')
    #Calculate log returns
    s['LogRet'] = (np.log(s['Close']/s['Close'].shift(1)))
    #Time series statistics
    s['Mean'] = (np.mean(s['LogRet'])*252)
    s['SD'] = (np.std(s['LogRet'])*np.sqrt(252))
    s['InfoRat'] = (s['Mean'].tail(1)-bmk['Mean'].tail(1))/s['SD'].tail(1)
    #Info ratio statistic
    print(s['InfoRat'].dropna())
  
#for all tickers
for s in symbols:
    try:
        #Print ticker and info ratio
        print(s, (InfoRat(s)))
    
    except OSError:
        pass
