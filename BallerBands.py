"""
Spyder Editor
"""

#pandas_datareader is deprecated, use YahooGrabber
#These are Bollinger Bands, a technical analysis tool

from pandas_datareader import data
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='1/1/2015', end='01/01/2050')
window = 20
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
s = s[window:]
s[['Adj Close', 'nDaySMA', 'UpperBand', 'LowerBand']].plot(grid=True,
                                                           figsize=(8, 5))
