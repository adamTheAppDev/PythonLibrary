# -*- coding: utf-8 -*-
"""

@author: Andreas Meuller and Guido

"""

#Supervised Learning Binary Classification Wisconsin Data Ridge Regression
#This model is from the Muller and Guido Python ML book

#Import modules
#import sys
#import sklearn
#import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#from scipy import sparse
#import pandas as pd
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import mglearn
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression

#Load data; X is features 13 OG features and 91 interactions, y is median price value 
X, y = mglearn.datasets.load_extended_boston()

#Display info
print("Data shape: {}".format(X.shape))
print("--------------------------------")

#Split train/test data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#Fit linear regression model
lr = LinearRegression().fit(X_train, y_train)

#Training dataset
print("Linear Regression")
print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#Test set
print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))
print("--------------------------------")

#Fit ridge regression model
ridge = Ridge().fit(X_train, y_train)

#Training dataset
print("Ridge A1 Regression")
print("Training set score: {:.2f}".format(ridge.score(X_train, y_train)))
#Test set
print("Test set score: {:.2f}".format(ridge.score(X_test, y_test)))
print("--------------------------------")

#Alpha param 10
#Refit with new alpha param value
ridge10 = Ridge(alpha=10).fit(X_train, y_train)
print("Ridge A10 Regression")
print("Training set score: {:.2f}".format(ridge10.score(X_train, y_train)))
print("Test set score: {:.2f}".format(ridge10.score(X_test, y_test)))
print("--------------------------------")

#Alpha param .1
#Refit with new alpha param value
ridge01 = Ridge(alpha=0.1).fit(X_train, y_train)
print("Ridge A.1 Regression")
print("Training set score: {:.2f}".format(ridge01.score(X_train, y_train)))
print("Test set score: {:.2f}".format(ridge01.score(X_test, y_test)))
print("--------------------------------")

#Compare coefficient magnitudes for linear vs ridge with varying alpha
plt.plot(ridge.coef_, 's', label="Ridge alpha=1")
plt.plot(ridge10.coef_, '^', label="Ridge alpha=10")
plt.plot(ridge01.coef_, 'v', label="Ridge alpha=0.1")
plt.plot(lr.coef_, 'o', label="LinearRegression")
#Labels
plt.xlabel("Coefficient index")
plt.ylabel("Coefficient magnitude")
#Horizontal black line
plt.hlines(0, 0, len(lr.coef_))
plt.ylim(-25, 25)
plt.legend()
