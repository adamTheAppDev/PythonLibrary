# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic + database query tool

#Import modules
import numpy as np
#Define function
def SCoeffVar(s):
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate average returns
    s['Mean'] = np.mean(s['LogRet'])*252
    #Calculate standard deviation
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    #Calculate coefficient of variation
    s['CoeffVar'] = s['SD']/s['Mean']
    #Output
    return s['CoeffVar'].tail(1)
