"""
Spyder Editor
"""

from pandas_datareader import data
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2017', end='01/01/2050')
window = 20
s['nDaySMA'] = s['Adj Close'].rolling(window=window, center=False).mean()
s['nDaySTD'] = s['Adj Close'].rolling(window=window, center=False).std()
s['UpperBand'] = s['nDaySMA'] + (s['nDaySTD'] * 2)
s['LowerBand'] = s['nDaySMA'] - (s['nDaySTD'] * 2)
s['B'] = (s['Adj Close'] - s['LowerBand'])/(s['UpperBand'] - s['LowerBand'])
s = s[window:]
s['B'].plot(grid=True, figsize=(8, 3))