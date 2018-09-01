# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 00:29:28 2017

@author: AmatVictoriaCuramIII
"""

#Div Yield Approximation
def DividendYield(ticker):
    from YahooGrabber import YahooGrabber
    from YahooDivGrabber import YahooDivGrabber
    priceInfo = YahooGrabber(ticker)
    dividendInfo = YahooDivGrabber(ticker)
    lastPrice = priceInfo['Adj Close'][-1]
    lastDividend = dividendInfo['Dividends'][-1]
    divYield = lastDividend/lastPrice
    return divYield