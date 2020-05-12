# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a probability of touch calculator based on a random normal distribution
#Equities over longer periods of time may be log normally distributed
#Equities over shorter periods of time may be normally or uniformly distributed

#Import modules
import scipy.stats as sp
import numpy as np
from pandas_datareader import data

#Define function
def ProbTouch(s, price, distance):
    #Mean + STD factor
    factor = 1
    #Period length - used in creating distribution
    timesteps = 252
    #Length of simulation
    periods = list(range(1, distance+1))
    #Request data
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    #Graphical display
    s['Close'].plot(grid=True, figsize=(8, 5))
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Average return
    s['Mean'] = np.round((np.mean(s['LogRet'])), 5)* Factor
    #Standard deviation
    s['SD'] = np.std(s['LogRet'])*np.sqrt(factor)
    #Variable assignment
    mu = s['Mean'].tail(1)
    sigma = s['SD'].tail(1)
    #Create normal distribution
    distribution = np.random.normal(mu, sigma, timesteps)
    #Last close price data
    seedprice = s['Adj Close'].tail(1)
    newseed = seedprice[0]
    #Empty list
    relist = []
    #Simulation - for all values in distribution
    for d in distribution:
        #Ending price
        destination = newseed + (newseed * d)
        #Add to list
        relist.append(destination)
        #Reassign ending price
        newseed = destination  
    #Stats for relist
    sumlist = []
    #For each step in length of simulation
    for p in periods:
        z = (np.log((price/seedprice[0]))/((sigma * np.sqrt(252)* np.sqrt(
                                                                    p/252))))
        x = sp.norm.cdf(z)
        y = 1 - x 
        if price > seedprice[0]:
            sumlist.append(y)
        else:
            sumlist.append(x)  
    #Probability of touch
    ProbTouch = sumlist[-1]
    return ProbTouch
