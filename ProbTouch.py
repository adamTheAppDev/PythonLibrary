# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 23:51:14 2016

@author: AmatVictoriaCuramIII
"""

#This is a probability of touch calculator based on a random normal distribution
#Equities over longer periods of time may be log normally distributed
#Equities over shorter periods of time may be normally or uniformly distributed


import scipy.stats as sp
import numpy as np
from pandas_datareader import data
def ProbTouch(s, price, distance):
    period = 1
    timesteps = 252
    poweranger = list(range(1, distance+1))#distance+1
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['Close'].plot(grid=True, figsize=(8, 5))
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.round((np.mean(s['LogRet'])), 5)*period
    s['SD'] = np.std(s['LogRet'])*np.sqrt(period)
    mu = s['Mean'].tail(1)
    sigma = s['SD'].tail(1)
    distribution = np.random.normal(mu, sigma, timesteps)
    seedprice = s['Adj Close'].tail(1)
    newseed = seedprice[0]
    relist = []
#simulation
    for d in distribution:
        destination = newseed + (newseed * d)
        relist.append(destination)
        newseed = destination  
#get stats for relist
    sumlist = []
#        sigma1 = np.std(relist)
    for p in poweranger:
        z = (np.log((price/seedprice[0]))/((sigma * np.sqrt(252)* np.sqrt(
                                                                    p/252))))
        x = sp.norm.cdf(z)
        y = 1 - x 
        if price > seedprice[0]:
            sumlist.append(y)
        else:
            sumlist.append(x)       
    ProbTouch = sumlist[-1]
    return ProbTouch
