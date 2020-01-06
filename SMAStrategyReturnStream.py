# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:47:07 2018

@author: Adam Reinhold Von Fisher - adamrvfisher@gmail.com 
linkedin.com/in/adamrvfisher - github.com/adamrvfisher/TechnicalAnalysisLibrary
"""
def SMAStrategyReturnStream(winners, shortest):
#Dual Asset SMA Strategy Return Stream Generator
    import numpy as np
    import pandas as pd
    from DatabaseGrabber import DatabaseGrabber
#    from YahooGrabber import YahooGrabber
    
    Ticker1 = winners[10]
    Ticker2 = winners[11]

    Portfolio = pd.DataFrame()
    #pull online data, change to local for testing
    Asset1 = DatabaseGrabber(Ticker1)
    Asset2 = DatabaseGrabber(Ticker2)    
    #get log returns
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
    Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
    #Match lengths
    Asset1 = Asset1[-shortest:]
    Asset2 = Asset2[-shortest:]
    #
    
    a = winners[0]
    b = winners[1]
    c = winners[2]
    d = winners[3]
    e = winners[4]
    f = winners[5]
    
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=e, center=False).mean()
    Asset2['MA'] = Asset2['Adj Close'].rolling(window=f, center=False).mean()        
    
            
    
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Asset1['Adj Close'].shift(1) > Asset1['MA'].shift(1),
                                    c,a)                                    
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    
    Asset2['Position'] = b
    Asset2['Position'] = np.where(Asset2['Adj Close'].shift(1) > Asset2['MA'].shift(1),
                                    d,b)
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    
    Portfolio['Asset1Pass'] = (Asset1['Pass']) #* (-1) #Pass a short position?
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1) #Pass a short position?
    Portfolio['ReturnStream'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
    
    return Portfolio['ReturnStream'] 