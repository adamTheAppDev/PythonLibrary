# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:28:54 2019

@author: AmatVictoriaCuramIII
"""

#This is from a book written in part by https://github.com/amueller 
#Easy linear regression using the mglearn datasets

from sklearn.linear_model import LinearRegression
import mglearn
from sklearn.model_selection import train_test_split

#load data
X, y = mglearn.datasets.make_wave(n_samples=60)

#split train/test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

#fit linear model
lr = LinearRegression().fit(X_train, y_train)

#linear regression outputs
print("lr.coef_: {}".format(lr.coef_))
print("lr.intercept_: {}".format(lr.intercept_))

#performance metrics
#training set
print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#test set
print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))
