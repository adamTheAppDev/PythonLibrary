"""
Spyder Editor
"""
from scipy.stats import linregress
from pandas_datareader import data
s = data.DataReader('^GSPC', 'yahoo', start='1/1/2001', end='01/01/2050')
x = range(len(s))
y = s['Adj Close']
slope, intercept, r_value, p_value, std_err = linregress(x,y)
s['Linear Regression'] = slope*x+intercept
s[['Adj Close','Linear Regression']].plot(grid = True, figsize = (8,5))
