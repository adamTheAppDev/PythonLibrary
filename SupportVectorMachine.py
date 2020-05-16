# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a single feature/dimension support vector machine - not dissimilar results from a linear regression

#SVR - RBF
#Import modules
import numpy as np
import matplotlib.pyplot as plt
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
from YahooGrabber import YahooGrabber
from sklearn.svm import SVR

#Request data 
ticker = YahooGrabber('UVXY')

#Variable assignment
trim = 50

#Time series trimmer
ticker = ticker[-200:-150]

#Dates object
dates =  np.array(ticker.index)
#Format
dates = np.reshape(dates, (len(dates),1))
#Prices object
prices = ticker['Adj Close']
#Format
prices = np.reshape(prices, (len(prices),1))

#Model types
#svr_lin = SVR(kernel = 'linear', C = 1e3)
#svr_poly = SVR(kernel = 'poly', C = 1e3, degree = 2)
svr_rbf = SVR(kernel = 'rbf', C = 1e3, epsilon = .2, gamma = .1)
#svr_lin.fit(dates, prices)
#svr_poly.fit(dates, prices)
svr_rbf.fit(dates, prices)

#Graphical display
plt.scatter(dates, prices, color = 'black', label = 'Data')
plt.plot(dates, svr_rbf.predict(dates), color = 'red', label = 'RBF model')
#plt.plot(dates, svr_lin.predict(dates), color = 'blue', label = 'Linear model')
#plt.plot(dates, svr_poly.predict(dates), color = 'green', label = 'Polynomial model')

#Model results
#print('r^2 = ', svr_rbf.score(dates, prices))

#Add labels
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

#Display results
#print('Lin: ', svr_lin.predict(0))
#print('Poly: ', svr_poly.predict(0))
print('RBF: ', svr_rbf.predict(trim)[0])
