# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 08:00:58 2017

@author: AmatVictoriaCuramIII
"""
#menu selection lab
print('1. Calculate the area of a circle.')
print('2. Calculate the area of a rectangle.')
print('3. Calculate the area of a triangle.')
print('4. Quit.')
print('Enter your choice 1-4.')
choice = int(input(""))
while choice < 1 or choice > 4:
    print('Sorry, that is an invalid selection.')
    print('Enter your choice 1-4.')
    choice = int(input(""))
if choice == 4:
    pass
elif choice == 1:
    print('Enter the radius of your circle')
    radius = input("")
    realradius = float(radius)
    pie = 3.14159
    area = pie*(realradius**2)
    print('The area of your circle is ', area, ' units.')
elif choice == 2:
    print('Enter the length of your rectangle.')
    length = input("")
    reallength = float(length)
    print('Enter the width of your rectangle.')
    width = input("")
    realwidth = float(width)  
    area = reallength * realwidth
    print('The area of your rectangle is ', area, ' units.')
elif choice == 3:
    print('Enter the length of your triangle base.')
    length = input("")
    reallength = float(length)
    print('Enter the height of your triangle.')
    height = input("")
    realheight = float(height)  
    area = reallength * realheight * .5
    print('The area of your rectangle is ', area, ' units.')    
    
    