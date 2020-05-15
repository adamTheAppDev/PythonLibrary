# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a much faster EMA calculation using np.convolve 
#pandas_datareader is deprecated, use YahooGrabber

#Import modules
from pandas_datareader import data
import numpy as np
#Assign ticker
ticker = '^GSPC'

#Request data
uuu = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050')

#Variable assignment
emawindow = 25
ema2window = 50
values = uuu['Adj Close']
#Calculate EMA
weights = np.repeat(1.0, emawindow)/emawindow
weights2 = np.repeat(1.0, ema2window)/ema2window
smas = np.convolve(values, weights, 'valid')
smas2 = np.convolve(values, weights2, 'valid')

#Trim lengths
trim = len(uuu) - len(smas2)
trim2 = len(smas) - len(smas2)
#Replace missing data
replace = uuu[:trim]
#Trim lengths
uuu = uuu[trim:]
smas = smas[trim2:]
#Assign EMAs
uuu['EMAS'] = smas
uuu['EMAS2'] = smas2
#Replace missing data
uuu = replace.append(uuu)
