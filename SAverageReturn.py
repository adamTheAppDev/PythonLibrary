# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Import modules
import numpy as np
#Define function
def SAverageReturn(s):
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate average
    s['Mean'] = np.mean(s['LogRet'])*252
    #Output
    return s['Mean'].tail(1)
