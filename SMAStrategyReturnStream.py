# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Dual Asset SMA Strategy Return Stream Generator
#This is a return stream generator for a two asset portfolio based on params from
#a separate optimization

#Define function
def SMAStrategyReturnStream(winners, shortest):
    #Import modules
    import numpy as np
    import pandas as pd
    from DatabaseGrabber import DatabaseGrabber
    #Read in tickers from params
    Ticker1 = winners[10]
    Ticker2 = winners[11]
    #Empty data structure
    Portfolio = pd.DataFrame()
    #Request data
    Asset1 = DatabaseGrabber(Ticker1)
    Asset2 = DatabaseGrabber(Ticker2)    
    #Calculate log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
    Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
    #Time series trimmer
    Asset1 = Asset1[-shortest:]
    Asset2 = Asset2[-shortest:]
    
    #Read in params
    a = winners[0]
    b = winners[1]
    c = winners[2]
    d = winners[3]
    e = winners[4]
    f = winners[5]
    
    #Calculate simple moving averages
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
    Asset2['MA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()        
    
    #Position sizing
    Asset1['Position'] = a
    #Alternative position sizing
    Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['MA'].shift(1),
                                    c,a)                        
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    #Alternative position sizing
    Asset2['Position'] = np.where(Asset2['Adj Close'].shift(1) > Asset2['MA'].shift(1),
                                    d,b)
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position?
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position?
    #Two asset return stream
    Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
    #Output
    return Portfolio['ReturnStream'] 
