# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic calculator
#Add more tickers as needed

from YahooGrabber import YahooGrabber
import pandas as pd
import numpy as np

#Variable assignment
tickers = ['^RUT','GLD','SOYB','JO','TLT']
returns = pd.DataFrame()

#For all tickers
for s in tickers:
    #Data request
    s = YahooGrabber(s)
    #Calculate returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Put returns in DataFrame
    returns = pd.concat([returns,s['LogRet']],axis = 1)

#Assign column names -- BEWARE -- if there are any missing data sets column names will be spurious
#Need to assign column names as returns table is populated in for loop.
returns.columns = tickers
#Fill nans with 0
returns = returns.fillna(0)
#Calculate correlation matrix
matrix = returns.corr()
#Display
print(matrix)
