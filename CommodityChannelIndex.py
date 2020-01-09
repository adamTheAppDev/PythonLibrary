"""
Spyder Editor
"""

#This is a technical analysis tool

from DatabaseGrabber import DatabaseGrabber
ticker = 'IWM'
constant = .02
SMAwindow = 20
s = DatabaseGrabber(ticker)
s['TP'] = (s['High'] + s['Low'] + s['Adj Close']) / 3
s['TPSMA'] = s['TP'].rolling(center=False, window = SMAwindow).mean()
s['MeanDeviation'] = s['TP'].rolling(center=False, window = SMAwindow).std()
s['CCI'] = ((s['TP'] - s['TPSMA'])/(constant*s['MeanDeviation']))
s['Top'] = 100
s['Bottom'] = -100
s = s[SMAwindow:]
s[['CCI','Top','Bottom']].plot(grid = True, figsize = (8,3))
