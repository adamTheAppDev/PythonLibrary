# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:45:20 2017

@author: AmatVictoriaCuramIII
"""

def main():
    payRate = getValidRate()
    hours = getValidHours()
    calcAndDisplayGrossPay(payRate,hours)
    
def getValidRate():
    print("Please enter your hourly wage rate.")
    hourlyWageRate = input("")
    realHWR = float(hourlyWageRate)
    while realHWR < 7.5 or realHWR >18.25:
        print("Invalid input, please enter your hourly wage rate.")
        hourlyWageRate = input("")
        realHWR = float(hourlyWageRate)
        if realHWR >= 7.5 and realHWR <= 18.25:
            return realHWR
            
def getValidHours():
    print("Please enter the number of hours worked.")
    hoursWorked = input("")
    realHoursWorked = float(hoursWorked)
    while realHoursWorked < 0 or realHoursWorked > 40:
        print("Invalid input, please enter the number of hours you worked.")
        hoursWorked = input("")
        realHoursWorked = float(hoursWorked)
        if realHoursWorked >= 0 and realHoursWorked <= 40:
            return realHoursWorked

def calcAndDisplayGrossPay(payRate, hours):    
    grossPay = payRate * hours
    print("The gross pay is ", grossPay)
    
main()