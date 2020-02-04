# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a technical analysis tool

#import modules
from YahooGrabber import YahooGrabber

#input ticker
ticker = '^GSPC'
#Request data
s = YahooGrabber(ticker)
#Variable assignment
window = 20
#Rolling statistics
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()
#Define bands
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
#Difference between Adj Close and Lower band normalized by band width
s['B'] = (s['Adj Close'] - s['LowerBand'])/(s['UpperBand'] - s['LowerBand'])
#Trim window off for indicator display
s = s[window:]
#Graphical display
s['B'].plot(grid=True, figsize=(8, 3))
