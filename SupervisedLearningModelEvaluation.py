# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 05:33:49 2020

@author: AmatVictoriaCuramIII
"""

#Supervised Learning FDL Data Model Evaluation - Continuous Data

#Import modules
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoLars
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from YahooSourceDailyGrabber import YahooSourceDailyGrabber

#Grab localhost data
data = YahooSourceDailyGrabber('TQQQ')
#Add supplementary data
dataII = YahooSourceDailyGrabber('GLD')
dataIII = YahooSourceDailyGrabber('TLT')
dataIV = YahooSourceDailyGrabber('^VIX')
#trim data to match length
dataII = dataII[-len(data):]
dataIII = dataIII[-len(data):]
dataIV = dataIV[-len(data):]

#X is features n OG features, y is log returns 
#Levered equities
X = np.array(data[['8wkBreakOutRatio', '8wkBreakDownRatio', '4wkBreakOutRatio', 
'4wkBreakDownRatio', '2wkBreakOutRatio', '2wkBreakDownRatio', 'HigherOpen', 'LowerOpen',
'HigherHigh', 'LowerHigh', 'HigherLow', 'LowerLow', 'HigherClose', 'LowerClose','GapUp',
'GapDown','8wkRangePercent', '4wkRangePercent', '2wkRangePercent', '8wkRollingAverageRange',
'4wkRollingAverageRange', '2wkRollingAverageRange', '8wkRARtoTAR', '4wkRARtoTAR',
'2wkRARtoTAR', '8wkRollingAverageReturn', '4wkRollingAverageReturn', '2wkRollingAverageReturn',
'8wkRollingStdDev', '4wkRollingStdDev', '2wkRollingStdDev', '8wkRateOfChange', '4wkRateOfChange',
'2wkRateOfChange', '8wkRollingAverageVolume', '4wkRollingAverageVolume' ,'2wkRollingAverageVolume',
'8wkRollingReturnOverAverage', '4wkRollingReturnOverAverage', '2wkRollingReturnOverAverage',
'8wkRollingStdDevOverAverage', '4wkRollingStdDevOverAverage', '2wkRollingStdDevOverAverage',
'8wkATRPercent','4wkATRPercent', '2wkATRPercent','8wkRAATRtoTAATR', '4wkRAATRtoTAATR',
'2wkRAATRtoTAATR', '8wkATRtoRange', '4wkATRtoRange', '2wkATRtoRange', '8wkRollingAverageATRtoRange',
'4wkRollingAverageATRtoRange', '2wkRollingAverageATRtoRange', '8wkEfficiency', 
'4wkEfficiency', '2wkEfficiency']][50:].fillna(0))
#Gold
XII = np.array(dataII[['8wkBreakOutRatio', '8wkBreakDownRatio', '4wkBreakOutRatio', 
'4wkBreakDownRatio', '2wkBreakOutRatio', '2wkBreakDownRatio', 'HigherOpen', 'LowerOpen',
'HigherHigh', 'LowerHigh', 'HigherLow', 'LowerLow', 'HigherClose', 'LowerClose','GapUp',
'GapDown','8wkRangePercent', '4wkRangePercent', '2wkRangePercent', '8wkRollingAverageRange',
'4wkRollingAverageRange', '2wkRollingAverageRange', '8wkRARtoTAR', '4wkRARtoTAR',
'2wkRARtoTAR', '8wkRollingAverageReturn', '4wkRollingAverageReturn', '2wkRollingAverageReturn',
'8wkRollingStdDev', '4wkRollingStdDev', '2wkRollingStdDev', '8wkRateOfChange', '4wkRateOfChange',
'2wkRateOfChange', '8wkRollingAverageVolume', '4wkRollingAverageVolume' ,'2wkRollingAverageVolume',
'8wkRollingReturnOverAverage', '4wkRollingReturnOverAverage', '2wkRollingReturnOverAverage',
'8wkRollingStdDevOverAverage', '4wkRollingStdDevOverAverage', '2wkRollingStdDevOverAverage',
'8wkATRPercent','4wkATRPercent', '2wkATRPercent','8wkRAATRtoTAATR', '4wkRAATRtoTAATR',
'2wkRAATRtoTAATR', '8wkATRtoRange', '4wkATRtoRange', '2wkATRtoRange', '8wkRollingAverageATRtoRange',
'4wkRollingAverageATRtoRange', '2wkRollingAverageATRtoRange', '8wkEfficiency', 
'4wkEfficiency', '2wkEfficiency']][50:].fillna(0))
#30 year Bonds
XIII = np.array(dataIII[['8wkBreakOutRatio', '8wkBreakDownRatio', '4wkBreakOutRatio', 
'4wkBreakDownRatio', '2wkBreakOutRatio', '2wkBreakDownRatio', 'HigherOpen', 'LowerOpen',
'HigherHigh', 'LowerHigh', 'HigherLow', 'LowerLow', 'HigherClose', 'LowerClose','GapUp',
'GapDown','8wkRangePercent', '4wkRangePercent', '2wkRangePercent', '8wkRollingAverageRange',
'4wkRollingAverageRange', '2wkRollingAverageRange', '8wkRARtoTAR', '4wkRARtoTAR',
'2wkRARtoTAR', '8wkRollingAverageReturn', '4wkRollingAverageReturn', '2wkRollingAverageReturn',
'8wkRollingStdDev', '4wkRollingStdDev', '2wkRollingStdDev', '8wkRateOfChange', '4wkRateOfChange',
'2wkRateOfChange', '8wkRollingAverageVolume', '4wkRollingAverageVolume' ,'2wkRollingAverageVolume',
'8wkRollingReturnOverAverage', '4wkRollingReturnOverAverage', '2wkRollingReturnOverAverage',
'8wkRollingStdDevOverAverage', '4wkRollingStdDevOverAverage', '2wkRollingStdDevOverAverage',
'8wkATRPercent','4wkATRPercent', '2wkATRPercent','8wkRAATRtoTAATR', '4wkRAATRtoTAATR',
'2wkRAATRtoTAATR', '8wkATRtoRange', '4wkATRtoRange', '2wkATRtoRange', '8wkRollingAverageATRtoRange',
'4wkRollingAverageATRtoRange', '2wkRollingAverageATRtoRange', '8wkEfficiency', 
'4wkEfficiency', '2wkEfficiency']][50:].fillna(0))
#Volatility
XIV = np.array(dataIV[['8wkBreakOutRatio', '8wkBreakDownRatio', '4wkBreakOutRatio', 
'4wkBreakDownRatio', '2wkBreakOutRatio', '2wkBreakDownRatio', 'HigherOpen', 'LowerOpen',
'HigherHigh', 'LowerHigh', 'HigherLow', 'LowerLow', 'HigherClose', 'LowerClose','GapUp',
'GapDown','8wkRangePercent', '4wkRangePercent', '2wkRangePercent', '8wkRollingAverageRange',
'4wkRollingAverageRange', '2wkRollingAverageRange', '8wkRARtoTAR', '4wkRARtoTAR',
'2wkRARtoTAR', '8wkRollingAverageReturn', '4wkRollingAverageReturn', '2wkRollingAverageReturn',
'8wkRollingStdDev', '4wkRollingStdDev', '2wkRollingStdDev', '8wkRateOfChange', '4wkRateOfChange',
'2wkRateOfChange', '8wkRollingAverageVolume', '4wkRollingAverageVolume' ,'2wkRollingAverageVolume',
'8wkRollingReturnOverAverage', '4wkRollingReturnOverAverage', '2wkRollingReturnOverAverage',
'8wkRollingStdDevOverAverage', '4wkRollingStdDevOverAverage', '2wkRollingStdDevOverAverage',
'8wkATRPercent','4wkATRPercent', '2wkATRPercent','8wkRAATRtoTAATR', '4wkRAATRtoTAATR',
'2wkRAATRtoTAATR', '8wkATRtoRange', '4wkATRtoRange', '2wkATRtoRange', '8wkRollingAverageATRtoRange',
'4wkRollingAverageATRtoRange', '2wkRollingAverageATRtoRange', '8wkEfficiency', 
'4wkEfficiency', '2wkEfficiency']][50:].fillna(0)) 
#Append extra data 
X = np.append(X, XII, 1)
X = np.append(X, XIII, 1)
X = np.append(X, XIV, 1)
#data is trimmed due to calculation windows
y = np.array(data['LogRet'][50:])
#display info
print("Data shape: {}".format(X.shape))
print("--------------------------------")

#STRATIFIED K CROSS VALIDATION AKA RANDOM DATA - NON SEQUENTIAL LIKE IN KthFoldRSI_II.py
LinRegrScore = cross_val_score(LinearRegression(), X, y, cv = 5)
print('Linear Regression Average -- ', str(LinRegrScore.mean()))
LassoRegrScore = cross_val_score(Lasso(), X, y, cv = 5)
print('Lasso Regression Average -- ', str(LassoRegrScore.mean()))
RidgeRegrScore = cross_val_score(Ridge(), X, y, cv = 5)
print('Ridge Regression Average -- ', str(RidgeRegrScore.mean()))
SVRegrScore = cross_val_score(SVR(), X, y, cv = 5)
print('Support Vector Regression Average -- ', str(SVRegrScore.mean()))
LassoLARegrScore = cross_val_score(LassoLars(), X, y, cv = 5)
print('Lasso Least Angle Regression Average -- ', str(LassoLARegrScore.mean()))
DTreeScore = cross_val_score(DecisionTreeRegressor(), X, y, cv = 5)
print('Decision Tree Regression Average -- ', str(DTreeScore.mean()))
AdaBoostRegrScore = cross_val_score(AdaBoostRegressor(), X, y, cv = 5)
print('Ada Boost Regression Average -- ', str(AdaBoostRegrScore.mean()))
GradBoostRegrScore = cross_val_score(GradientBoostingRegressor(), X, y, cv = 5)
print('Gradient Boost Regression Average -- ', str(GradBoostRegrScore.mean()))
print("--------------------------------")
print("Perhaps it is time for some parameter tuning.")