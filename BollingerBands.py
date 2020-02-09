# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#These are Bollinger Bands, a technical analysis tool

#Import modules
from YahooGrabber import YahooGrabber
from pandas_datareader import data

#Input ticker
ticker = '^GSPC'
s = YahooGrabber(ticker)

#Variable assignment
window = 20

#SMA/STD calculation
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()
#Band calculation
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
#Trim data
s = s[window:]

#Graphical display
s[['Adj Close', 'nDaySMA', 'UpperBand', 'LowerBand']].plot(grid=True,
                                                           figsize=(8, 5))
