"""
Spyder Editor
"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a technical analysis tool

from pandas_datareader import data
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='11/01/2016', end='01/01/2050')
window = 20
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
s['BandWidth'] = ((s['UpperBand'] - s['LowerBand'])/s['nDaySMA'])*100
s = s[window:]
s['BandWidth'].plot(grid=True, figsize=(8, 3))
