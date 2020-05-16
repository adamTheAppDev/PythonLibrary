# -*- coding: utf-8 -*-
"""

@author: Andreas Mueller and Guido

"""

#Supervised Learning Regression 

#Import modules
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

#Generate data X and y, X is feature and y is target
X, y = mglearn.datasets.make_wave(n_samples=40)

#Split data - 'random' train/test selection
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#Instantiate the model and set the number of neighbors to consider to 3
reg = KNeighborsRegressor(n_neighbors=3)
#Fit the model using the training data and training targets
reg.fit(X_train, y_train)

#Test set predictions
print("Test set predictions:\n{}".format(reg.predict(X_test)))

#Test set R^2
print("Test set R^2: {:.2f}".format(reg.score(X_test, y_test)))

#Graph features
plt.plot(X, y, 'o')
#Graph constraints
plt.ylim(-3, 3)
#Labels
plt.xlabel("Feature")
plt.ylabel("Target")
