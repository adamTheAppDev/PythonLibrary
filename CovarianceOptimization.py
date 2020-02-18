# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 23:55:18 2017

@author: AmatVictoriaCuramIII
"""

#This is a portfolio statistic tool based on Markowitz mean variance optimization
#turn covariance matrix into max sharpe & minimum variance

#Import modules
import pandas as pd
from YahooGrabber import YahooGrabber
import numpy as np
import os
from RandomWeight import RandomWeight
from GenerateRandomPortfolio import GenerateRandomPortfolio

#Universe list for matric generation
listofstocks = ['^GSPC','^DJI','^RUT','^FVX', '^TNX','^NZ50','^STOXX','^FCHI',
'HYG','^MERV','^JKSE','^TYX','^BFX','^STI','^MXX','^HSI','^BSESN','KS11',
'^BVSP','^IPSA','^KLSE','USO','UNG','GLD','DBC','SOYB','JO','UUP']

#List to array
stocks = np.array(listofstocks)

#Variable assignment
df = pd.DataFrame()
ranger = range(0, len(listofstocks))

#For all stocks in universe
for i in ranger:
    try:
        #x is ticker name
        x = listofstocks[i]
        #Request data
        temp = YahooGrabber(x)
        #Delete duplicate rows
        temp = temp[~temp.index.duplicated(keep='first')]
        #Calculate log returns
        temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
        temp[x+'LogRet'] = temp['LogRet'] 
        temp[x+'LogRet'] = temp[x+'LogRet'].fillna(0)      
        #Add log returns to matrix for later calculation
        df = pd.concat([df,temp[x+'LogRet']],axis = 1)
    #This is for DatabaseGrabber not YahooGrabber
    except FileNotFoundError:
        continue
   
#Make directory for the log returns
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet')
    
#Store the log returns    
pd.to_pickle(df, 'F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet\\MiniUniverseLogRet')

#List of column headers
totalcolumns = ['Mean', 'StandardDeviation']
#Adding tickers to column headers
for l in df.columns:
    totalcolumns.append(l)
    
#Trimming returns     
df = df[-60:]
df = df.fillna(0)

#Calculate covariance
dfCov = df.cov()

#Make directory to store covariance matrix
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance')

#Store covariance matrix
pd.to_pickle(dfCov, 'F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance\\MiniUniverse12wkCovariance')

#Variable assignment
Iterations = 1
RangeIterations = range(0,Iterations)

#Column assignment
portfolios = pd.DataFrame(columns = totalcolumns)

#for one time only
for i in RangeIterations:
    #Average, STDev, weights
    mu, sigma, w = GenerateRandomPortfolio(df)    
    #Append columns 
    prep = np.concatenate([mu,sigma,w],axis=1)
    #Add to dataframe
    prepare = np.concatenate([portfolios,prep], axis = 0)
    #array to series
    prepare = pd.Series(prep)
    #Add to dataframe
    portfolios = pd.concat([portfolios,prepare], axis = 0)
print(portfolios)

#Optional save to directory
#pd.to_pickle(maxsharpe, 'F:\\Users\\AmatVictoriaCuram\\Database\\target\\target')
#pd.to_pickle(minvariance, 'F:\\Users\\AmatVictoriaCuram\\Database\\target\\target2')
