# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:02:03 2017

@author: AmatVictoriaCuramIII
"""
iteration = range(100)
for i in iteration:
    print("Please enter your hourly wage rate.")
    hourlyWageRate = input("")
    realHWR = float(hourlyWageRate)
    if realHWR < 7.5 or realHWR > 18.25:
        print('This is an invalid entry for wage rate.')
        continue
    print("Please enter the number of hours worked this week")
    numberHoursWorked = input("")
    realNHW = float(numberHoursWorked) 
    if realNHW < 0 or realNHW > 40:
        print('This is an invalid entry for hours worked.')
        continue
    break
grossPay = realHWR * realNHW
print("The gross pay for this week is ", grossPay)