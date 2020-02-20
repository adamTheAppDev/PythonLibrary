# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool for portfolio analysis
#Covariance matrix

#Import modules
import pandas as pd
import os

#Read in preprocessed log returns 
logret = pd.read_pickle('F:\\Users\\Username\\DirectoryLocation\\UniverseLogRet\\UniverseLogRet')
#Trim
logret = logret[-60:]

#Calculate covariance
matrix = logret.cov()

#Make storage place
if not os.path.exists('F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance'):
    os.makedirs('F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance')

#Store via pickle
pd.to_pickle(matrix, 'F:\\Users\\Username\\DirectoryLocation\\UniverseCovariance\\Universe12wkCovariance')
