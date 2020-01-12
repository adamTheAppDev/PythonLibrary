# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 19:04:59 2019

@author: AmatVictoriaCuramIII
"""

#This is from the https://github.com/amueller and Guido Python ML book
#Supervised Learning Binary Classification Wisconsin Data Linear Regression

#import sys
#import sklearn
#import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
#from scipy import sparse
#import matplotlib.pyplot as plt
#import pandas as pd
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import mglearn
from sklearn.linear_model import LinearRegression

#load data; X is features 13 OG features and 91 interactions, y is median price value 
X, y = mglearn.datasets.load_extended_boston()

#display info
print("Data shape: {}".format(X.shape))
print("--------------------------------")

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#fit linear model
lr = LinearRegression().fit(X_train, y_train)

#training dataset
print("Training set score: {:.2f}".format(lr.score(X_train, y_train)))
#test set
print("Test set score: {:.2f}".format(lr.score(X_test, y_test)))

