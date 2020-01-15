# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 19:04:59 2019

@author: AmatVictoriaCuramIII
"""

#This is a ML model applied to price/technical data - X values are highly correlated, need to diversify features in production
#Supervised Learning FDL Data Ridge Regression

#import sys
#import sklearn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from scipy import sparse
#import pandas as pd
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
#from YahooGrabber import YahooGrabber
from YahooSourceDailyGrabber import YahooSourceDailyGrabber

#load data; 
data = YahooSourceDailyGrabber('TQQQ')

columntuple = tuple(data.columns[25:])
#X is features n OG features and nn interactions, y is price 

X = np.array(data[['8wkBreakOutRatio', '8wkBreakDownRatio', '7wkBreakOutRatio', '7wkBreakDownRatio', '6wkBreakOutRatio', '6wkBreakDownRatio', '5wkBreakOutRatio', '5wkBreakDownRatio', '4wkBreakOutRatio', '4wkBreakDownRatio', '3wkBreakOutRatio', '3wkBreakDownRatio', '2wkBreakOutRatio', '2wkBreakDownRatio', '1wkBreakOutRatio', '1wkBreakDownRatio']][50:].fillna(0))

y = np.array(data['Adj Close'][50:])

#display info
print("Data shape: {}".format(X.shape))
print("--------------------------------")

#split train/test data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#fit linear regression model
lr = LinearRegression().fit(X_train, y_train)

#training dataset
print("Linear Regression")
print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#test set
print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))
print("--------------------------------")

#fit ridge regression model
ridge = Ridge().fit(X_train, y_train)

#training dataset
print("Ridge A1 Regression")
print("Training set score: {:.2f}".format(ridge.score(X_train, y_train)))
#test set
print("Test set score: {:.2f}".format(ridge.score(X_test, y_test)))
print("--------------------------------")

#alpha param 10
#refit with new alpha param value
ridge10 = Ridge(alpha=10).fit(X_train, y_train)
print("Ridge A10 Regression")
print("Training set score: {:.2f}".format(ridge10.score(X_train, y_train)))
print("Test set score: {:.2f}".format(ridge10.score(X_test, y_test)))
print("--------------------------------")

#alpha param .1
#refit with new alpha param value
ridge01 = Ridge(alpha=0.1).fit(X_train, y_train)
print("Ridge A.1 Regression")
print("Training set score: {:.2f}".format(ridge01.score(X_train, y_train)))
print("Test set score: {:.2f}".format(ridge01.score(X_test, y_test)))
print("--------------------------------")

#compare coefficient magnitudes for linear vs ridge with varying alpha
plt.plot(ridge.coef_, 's', label="Ridge alpha=1")
plt.plot(ridge10.coef_, '^', label="Ridge alpha=10")
plt.plot(ridge01.coef_, 'v', label="Ridge alpha=0.1")
plt.plot(lr.coef_, 'o', label="LinearRegression")
#labels
plt.xlabel("Coefficient index")
plt.ylabel("Coefficient magnitude")
#horizontal black line
plt.hlines(0, 0, len(lr.coef_))
plt.ylim(-25, 25)
plt.legend()
