# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a portfolio analysis tool, must have all tickers log returns in a table to run 
#Generate Random Portfolio

#Define function
def GenerateRandomPortfolio(logret):
    #Import modules
    import numpy as np
    from RandomWeight import RandomWeight
    import pandas as pd
    #This reads in a matrix of log returns from different issues - returns in columns by issue
    logret = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet\\MiniUniverseLogRet')
    #Trim time series
    logret = logret[-60:]
    logret = logret.fillna(0)
    #Expected return matrix
    p = np.asmatrix(np.mean(logret, axis = 0))
    #Weights matrix
    w = np.asmatrix(RandomWeight(logret.shape[1]))
    #Covariance matrix
    C = np.asmatrix(np.cov(logret,rowvar=False)) 
    #Weights times returns.transpose
    mu = w * p.T
    #StdDev 
    sigma = np.sqrt(w * C * w.T)
    #StdDev over two
    if sigma > 2:
        return GenerateRandomPortfolio(logret)
    return mu, sigma, w
