# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 19:04:59 2019

@author: AmatVictoriaCuramIII
"""

#Supervised Learning Binary Classification Wisconsin cancer Data
#Machine learning model from Intro to Machine Learning in Python bu Muller and Guido

#import sys
#import sklearn
import numpy as np
#import pandas as pd
#from scipy import sparse
import matplotlib.pyplot as plt
#import pandas as pd
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
#import mglearn
from sklearn.datasets import load_breast_cancer

#load up data froim import
cancer = load_breast_cancer()

#display info
print("cancer.keys(): \n{}".format(cancer.keys()))
print("--------------------------------")
print("Shape of cancer data: {}".format(cancer.data.shape))
print("--------------------------------")
print("Sample counts per class:\n{}".format(
      {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
print("--------------------------------")
print("Feature names:\n{}".format(cancer.feature_names))
print("--------------------------------")

#assign training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=66)
    
training_accuracy = []
test_accuracy = []

#give range for neighbors testing
neighbors_settings = range(1, 11)

#for each number of neighbors in range
for n_neighbors in neighbors_settings:
    #define model object?
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    #fit model to training data
    clf.fit(X_train, y_train)
    #record training set accuracy to list
    training_accuracy.append(clf.score(X_train, y_train))
    #record generalization (test set) accuracy
    test_accuracy.append(clf.score(X_test, y_test))
    
#separate series, same graph
plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
#labels
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
#legend
plt.legend()
