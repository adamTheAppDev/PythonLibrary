# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 23:55:18 2017

@author: AmatVictoriaCuramIII
"""

#turn covariance matrix into max sharpe & minimum variance
import pandas as pd
from DatabaseGrabber import DatabaseGrabber
import numpy as np
import os
from RandomWeight import RandomWeight
from GenerateRandomPortfolio import GenerateRandomPortfolio

listofstocks = ['^GSPC','^DJI','^RUT','^FVX', '^TNX','^NZ50','^STOXX','^FCHI',
'HYG','^MERV','^JKSE','^TYX','^BFX','^STI','^MXX','^HSI','^BSESN','KS11',
'^BVSP','^IPSA','^KLSE','USO','UNG','GLD','DBC','SOYB','JO','UUP']
stocks = np.array(listofstocks)
df = pd.DataFrame()
ranger = range(0, len(listofstocks))
for i in ranger:
    try:
        x = listofstocks[i]
        temp = DatabaseGrabber(x)
        temp = temp[~temp.index.duplicated(keep='first')]
        temp['LogRet'] = np.log(temp['Adj Close']/temp['Adj Close'].shift(1)) 
        temp[x+'LogRet'] = temp['LogRet'] 
        temp[x+'LogRet'] = temp[x+'LogRet'].fillna(0)            
        df = pd.concat([df,temp[x+'LogRet']],axis = 1)
    except FileNotFoundError:
        continue
    
if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet')
    
pd.to_pickle(df, 'F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseLogRet\\MiniUniverseLogRet')

totalcolumns = ['Mean', 'StandardDeviation']
for l in df.columns:
    totalcolumns.append(l)
    
df = df[-60:]
df = df.fillna(0)

dfCov = df.cov()

if not os.path.exists('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance'):
    os.makedirs('F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance')
    
pd.to_pickle(dfCov, 'F:\\Users\\AmatVictoriaCuram\\Database\\MiniUniverseCovariance\\MiniUniverse12wkCovariance')

Iterations = 1
RangeIterations = range(0,Iterations)

portfolios = pd.DataFrame(columns = totalcolumns)

for i in RangeIterations:
    mu, sigma, w = GenerateRandomPortfolio(df)    
    prep = np.concatenate([mu,sigma,w],axis=1)
    prepare = np.concatenate([portfolios,prep], axis = 0)
    prepare = pd.Series(prep)
    portfolios = pd.concat([portfolios,prepare], axis = 0)
#print(portfolios)
#
##pd.to_pickle(maxsharpe, 'F:\\Users\\AmatVictoriaCuram\\Database\\target\\target')
##pd.to_pickle(minvariance, 'F:\\Users\\AmatVictoriaCuram\\Database\\target\\target2')