# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""


#This is a summary statistic calculator

#Import modules
import numpy as np
from YahooGrabber import YahooGrabber

#Define function, param
def CoeffVar(s):
    #Request data
    s = YahooGrabber(s)
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Calculate average return
    s['Mean'] = np.mean(s['LogRet'])*252
    #Calculate STDev returns
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    #Calculate Coefficient of variation
    s['CoeffVar'] = s['SD']/s['Mean']
    #Output
    return s['CoeffVar'].tail(1)
