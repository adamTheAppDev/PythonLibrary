# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:36:09 2017

@author: AmatVictoriaCuramIII
"""
from pandas_datareader import data
import numpy as np
ticker = '^GSPC'
uuu = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050')
emawindow = 25
ema2window = 50
values = uuu['Adj Close']
weights = np.repeat(1.0, emawindow)/emawindow
weights2 = np.repeat(1.0, ema2window)/ema2window
smas = np.convolve(values, weights, 'valid')
smas2 = np.convolve(values, weights2, 'valid')
trim = len(uuu) - len(smas2)
trim2 = len(smas) - len(smas2)
replace = uuu[:trim]
uuu = uuu[trim:]
smas = smas[trim2:]
uuu['EMAS'] = smas
uuu['EMAS2'] = smas2
uuu = replace.append(uuu)