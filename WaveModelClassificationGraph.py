# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 19:04:59 2019

@author: AmatVictoriaCuramIII
"""

#Supervised Learning Regression

#import sys
#import sklearn
#import numpy as np
#import pandas as pd
#from scipy import sparse
import matplotlib.pyplot as plt
#import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import mglearn
#generate data X and y, X is feature and y is target
X, y = mglearn.datasets.make_wave(n_samples=40)

#split data - 'random' train/test selection
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#instantiate the model and set the number of neighbors to consider to 3
reg = KNeighborsRegressor(n_neighbors=3)
#fit the model using the training data and training targets
reg.fit(X_train, y_train)

#test set predictions
print("Test set predictions:\n{}".format(reg.predict(X_test)))

#test set R^2
print("Test set R^2: {:.2f}".format(reg.score(X_test, y_test)))

#graph features
plt.plot(X, y, 'o')
#graph constraints
plt.ylim(-3, 3)
#labels
plt.xlabel("Feature")
plt.ylabel("Target")