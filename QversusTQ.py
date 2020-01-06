# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 13:16:51 2019

@author: AmatVictoriaCuramIII
"""

#TQQQ v QQQ return comparison

#Import libraries
import numpy as np
#import random as rand
import pandas as pd
#import time as t
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
#import matplotlib.pyplot as plt
import warnings 
from YahooGrabber import YahooGrabber

Q = YahooSourceDailyGrabber('QQQ')
TQ = YahooSourceDailyGrabber('TQQQ')

Q['LogRet'] = np.log(Q['Adj Close']/Q['Adj Close'].shift(1)) 
Q['LogRet'] = Q['LogRet'].fillna(0)

TQ['LogRet'] = np.log(TQ['Adj Close']/TQ['Adj Close'].shift(1)) 
TQ['LogRet'] = TQ['LogRet'].fillna(0)

#Trimmer
#trim = len(TQ)
#Q = Q[-trim:]

