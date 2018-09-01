# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:24:51 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
import pandas.io.data as web
import pandas as pd
def SDSD(s):
    s = web.get_data_yahoo(s, start='1/1/1900', end='01/01/2018')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['SD'] = np.sqrt(pd.rolling_var(s['LogRet']*np.sqrt(252), window=252))
    s['SDSD'] = np.std(s['SD']*np.sqrt(252))
    return s['SDSD'].tail(1)