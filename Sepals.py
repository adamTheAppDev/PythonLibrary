# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:39:33 2019

@author: AmatVictoriaCuramIII
"""

#This is from the Muller and Guido Python ML book
#Supervised Learning - Multiclass Classification

#import sys
#import sklearn
import numpy as np
import pandas as pd
#from scipy import sparse
#import matplotlib.pyplot as plt
#import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

#Gather batch
iris_dataset = load_iris()

#Split data, randomly - (X, y) (Independent, dependent) (Features, classification)
#Data is ordered by classification, so it' necessary to randomize and split
X_train, X_test, y_train, y_test = train_test_split(
    iris_dataset['data'], iris_dataset['target'], random_state=0)
    
#Create dataframe from data in X_train
#Label the columns using the strings in iris_dataset.feature_names
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)

#Create a scatter matrix from the dataframe, color by y_train
pairplot = pd.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o',
    hist_kwds={'bins': 20}, s=60, alpha=.8)

#Determine number of neighbors   
knn = KNeighborsClassifier(n_neighbors=1)

#Build model on training set
knn.fit(X_train, y_train)

#New data from new unknown flower
X_new = np.array([[5, 2.9, 1, .2]])

#Generate prediction with new data above
prediction = knn.predict(X_new)
print("Prediction: {}".format(prediction))
print("Predicted target name: {}".format(
                                    iris_dataset['target_names'][prediction]))

#Generate predictions for test set
#y_pred = knn.predict(X_test)
#print("Test set predictions:\n {}".format(y_pred))

#See test set accuracy arithmetically 
#print("Test set score: {:.2f}".format(np.mean(y_pred == y_test)))

#Or, use this method without having to generate predictions for test set
print("Test set score: {:.2f}".format(knn.score(X_test, y_test)))
