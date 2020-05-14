# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
import pandas.io.data as web
import pandas as pd

#Define function
def SDSD(s):
    #Request data
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate standard deviation
    s['SD'] = np.sqrt(pd.rolling_var(s['LogRet']*np.sqrt(252), window=252))
    #Calculate standard deviation of standard deviation
    s['SDSD'] = np.std(s['SD']*np.sqrt(252))
    #Output
    return s['SDSD'].tail(1)
