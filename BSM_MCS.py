# -*- coding: utf-8 -*-
"""
@author: Yves Hilpisch
"""

#This is a Black Scholes model from Yves Hilpisch's book

#Define function
def bsm_call_value(S0, K, T, r, sigma):
    #Import modules
    from math import log, sqrt, exp
    from scipy import stats
    #Type formatting
    S0 = float(S0)
    #BSM formula
    d1 = (log(S0 / K) + (r + .5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r + .5 * sigma ** 2) * T) / (sigma * sqrt(T))
    value = (S0 * stats.norm.cdf(d1, 0.0, 1.0) - K * exp(-r * T)
                * stats.norm.cdf(d2, 0.0, 1.0))
    return value

#Import modules    
from time import time
from math import exp, sqrt, log
from random import gauss, seed
#Spot
S0 = 100
#Strike
K = 105
#Time in years
T = 1.0 
#risk free short rate
r = .05
#volatility factor
sigma = .2
seed(20000)
t0 = time()
M = 50
dt = T / M
I = 250000
print(bsm_call_value(S0, K, T, r, sigma))
#Montecarlo
#Simulating I paths with M timesteps
S = []
for i in range(I):
    path = []
    for t in range(M + 1):
        if t == 0:
            path.append(S0)
        else:
            z = gauss(0, 1)
            St = path[t - 1] * exp((r - .5 * sigma ** 2) * dt + sigma * 
                                    sqrt(dt) * z)
            path.append(St)
    S.append(path)

C0 = (exp(-r * T) * sum([max(path[-1] - K, 0) for path in S]) / I)
C0 = int(C0)
TT = time() - t0
print('Euro Option Value %7.3f', C0)
print('Duration in Seconds %7.3f', TT)
