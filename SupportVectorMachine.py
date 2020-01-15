# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 19:56:39 2019

@author: AmatVictoriaCuramIII
"""

#This ML model was stolen from the depths of the internet and modified to fit financial data..
#Its a single feature/dimension support vector machine - not dissimilar results from a lin regression
#with this limited number of features/dims

#SVR - RBF
#Import libraries
import numpy as np
import matplotlib.pyplot as plt
from YahooSourceDailyGrabber import YahooSourceDailyGrabber
from YahooGrabber import YahooGrabber
from sklearn.svm import SVR

ticker = YahooGrabber('UVXY')
#trimmer
trim = 50
ticker = ticker[-200:-150]
dates =  np.array(ticker.index)
dates = np.reshape(dates, (len(dates),1))

prices = ticker['Adj Close']
prices = np.reshape(prices, (len(prices),1))
#
#svr_lin = SVR(kernel = 'linear', C = 1e3)
#svr_poly = SVR(kernel = 'poly', C = 1e3, degree = 2)
svr_rbf = SVR(kernel = 'rbf', C = 1e3, epsilon = .2, gamma = .1)
#svr_lin.fit(dates, prices)
#svr_poly.fit(dates, prices)
svr_rbf.fit(dates, prices)

plt.scatter(dates, prices, color = 'black', label = 'Data')
plt.plot(dates, svr_rbf.predict(dates), color = 'red', label = 'RBF model')
#plt.plot(dates, svr_lin.predict(dates), color = 'blue', label = 'Linear model')
#plt.plot(dates, svr_poly.predict(dates), color = 'green', label = 'Polynomial model')


#print('r^2 = ', svr_rbf.score(dates, prices))

plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
#
#print('Lin: ', svr_lin.predict(0))
#print('Poly: ', svr_poly.predict(0))
print('RBF: ', svr_rbf.predict(trim)[0])
