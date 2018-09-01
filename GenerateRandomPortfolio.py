# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 00:57:19 2017

@author: AmatVictoriaCuramIII
"""

#Generate Random Portfolio
def GenerateRandomPortfolio(logret):
    import pandas as pd
    
    logret = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet\\MiniUniverseLogRet')
    logret = logret[-60:]
    logret = logret.fillna(0)
    import numpy as np
    from RandomWeight import RandomWeight
    p = np.asmatrix(np.mean(logret, axis = 0)) #expected return
    w = np.asmatrix(RandomWeight(logret.shape[1])) #weights
    C = np.asmatrix(np.cov(logret,rowvar=False)) #covar matrix
    
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)
    
    if sigma > 2:
        return GenerateRandomPortfolio(logret)
    return mu, sigma, w