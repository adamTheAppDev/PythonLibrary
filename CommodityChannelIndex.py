"""
Spyder Editor
"""

from pandas_datareader import data
ticker = 'GLD'
constant = .015
SMAwindow = 20
s = data.DataReader(ticker, 'yahoo', start='10/1/2016', end='01/01/2050')
s['TP'] = (s['High'] + s['Low'] + s['Adj Close']) / 3
s['TPSMA'] = s['TP'].rolling(center=False, window = SMAwindow).mean()
s['MeanDeviation'] = s['TP'].rolling(center=False, window = SMAwindow).std()
s['CCI'] = ((s['TP'] - s['TPSMA'])/(constant*s['MeanDeviation']))
s['Top'] = 100
s['Bottom'] = -100
s = s[SMAwindow:]
s[['CCI','Top','Bottom']].plot(grid = True, figsize = (8,3))