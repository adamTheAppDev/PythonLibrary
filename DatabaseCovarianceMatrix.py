# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool for portfolio analysis
#Covariance matrix

import pandas as pd
import os

logret = pd.read_pickle('F:\\Users\\Username\\DirectoryLocation\\UniverseLogRet\\UniverseLogRet')
logret = logret[-60:]

square = logret.cov()

if not os.path.exists('F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance'):
    os.makedirs('F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance')
    
pd.to_pickle(square, 'F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance\\Universe12wkCovariance')
