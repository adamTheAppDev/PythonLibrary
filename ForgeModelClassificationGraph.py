# -*- coding: utf-8 -*-
"""

@author: https://github.com/amueller/ 

"""

#This is a model from https://github.com/amueller/ 
#Supervised Learning - Two feature dataset with Binary Classification
#K Nearest Neighbor

#Import modules
#import sys
#import sklearn
#import numpy as np
#import pandas as pd
#from scipy import sparse
import matplotlib.pyplot as plt
#import pandas as pd
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import mglearn #this is built in code.. USE SCIKIT for real applications

#generate dataset of X and y, X data are 2 features, y data is binary classification
X, y = mglearn.datasets.make_forge()
#scatter plot of 2 features
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
#legend
plt.legend(["Class 0", "Class 1"], loc=4)
#labels
plt.xlabel("First feature")
plt.ylabel("Second feature")
#shape of independent variables, features are here
print("X.shape: {}".format(X.shape))

#split to test and training set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#assign classifier object
clf = KNeighborsClassifier(n_neighbors=3)
#fit the data 
clf.fit(X_train, y_train)
#print predictions = clf.predict(X_test)
print("Test set predictions: {}".format(clf.predict(X_test)))
#print accuracy = clf.score(X_test, y_test)
print("Test set accuracy: {:.2f}".format(clf.score(X_test, y_test)))

#Define figure and axis + num subplots
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
#For neighbors 1 3 9 make subplots
for n_neighbors, ax in zip([1, 3, 9], axes):
    #Fit method returns the object self, so we can instantiate
    #and fit in one line
    clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)

    #MG built in graphs...    
    mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=.4)
    mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
    #Titles and labels
    ax.set_title("{} neighbor(s)".format(n_neighbors))
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")
#Define what subplot area displays legend
axes[0].legend(loc=3)
