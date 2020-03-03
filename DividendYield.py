Learn more or give us feedback
# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool based on last dividend
#Dividend Yield Approximation

#Define function - input ticker
def DividendYield(ticker):
    #Import modules
    from YahooGrabber import YahooGrabber
    from YahooDivGrabber import YahooDivGrabber
    #Data requests
    priceInfo = YahooGrabber(ticker)
    dividendInfo = YahooDivGrabber(ticker)
    #Get last price
    lastPrice = priceInfo['Adj Close'][-1]
    #Get last dividend
    lastDividend = dividendInfo['Dividends'][-1]
    #Calculate dividend yield based on last price
    divYield = lastDividend/lastPrice
    #Output dividend yield
    return divYield
