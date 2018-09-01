# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:34:43 2017

@author: AmatVictoriaCuramIII
"""

#really gnarly covariance matrix
import pandas as pd
import os

logret = pd.read_pickle('F:\\Users\\AmatVictoriaCuram\\Database\\UniverseLogRet\\UniverseLogRet')
logret = logret[-60:]

square = logret.cov()

if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\UniverseCovariance'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\UniverseCovariance')
    
pd.to_pickle(square, 'F:\\Users\\AmatVictoriaCuram\\Database\\UniverseCovariance\\Universe12wkCovariance')