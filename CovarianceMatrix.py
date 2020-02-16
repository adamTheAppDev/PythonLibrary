# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a summary statistic tool
#Add more tickers as needed

#Import modules
from YahooGrabber import YahooGrabber
import numpy as np

#Variable assignment
tickers = ['^RUT','GLD','SOYB','JO','TLT']
returns = pd.DataFrame()

#For all tickers
for s in tickers:
    #Request data
    s = YahooGrabber(s)
    #Calculate returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    #Add returns to DataFrame
    returns = pd.concat([returns,s['LogRet']],axis = 1)
#Add tickers to columns -- BEWARE -- if there is missing data from data req. 
#Column names will be spurious
returns.columns = tickers
#Fill nans with 0
returns = returns.fillna(0)
#Calculate covariance 
matrix = returns.cov()
#Display
print(matrix)
