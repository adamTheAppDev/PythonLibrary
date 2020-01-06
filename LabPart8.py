# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:58:43 2017

@author: AmatVictoriaCuramIII
"""

#paint job estimator
def Main():
    GetInputsThenRun()
def GetInputsThenRun():
    print("Please the cost of your paint per gallon.")
    PaintCost = input("")
    CostOfPaint = float(PaintCost)
    print("Please enter the size of your wall.")
    WallSize = input("")
    SizeOfWall= float(WallSize)
    DoMath(CostOfPaint, SizeOfWall)
def DoMath(CostOfPaint, SizeOfWall):
    LaborHoursPerGallon = 8
    WallSpacePerGallon = 115
    CostOfLaborPerHour = 20
    PaintRequired = SizeOfWall / WallSpacePerGallon
    LaborHours = PaintRequired * LaborHoursPerGallon
    LaborCost = LaborHours * CostOfLaborPerHour
    TotalPaintCost = CostOfPaint * PaintRequired
    TotalCost = LaborCost + TotalPaintCost
    DisplayResults(PaintRequired,LaborCost,LaborHours,
                   TotalPaintCost,TotalCost)
def DisplayResults(PaintRequired,LaborCost,LaborHours,
                   TotalPaintCost,TotalCost):
    print("The number of gallons of paint required is ", PaintRequired)
    print("The amount of labor hours required is ", LaborHours)
    print("The total paint cost is ", TotalPaintCost, " Dollars")
    print("The Labor Cost is ", LaborCost, " Dollars")
    print("The total cost of the job is ",TotalCost," Dollars")
Main()