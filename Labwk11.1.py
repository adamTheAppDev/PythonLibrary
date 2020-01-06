# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 08:43:33 2017

@author: AmatVictoriaCuramIII
"""
#menu selection lab pt 2
print('        Select a planet')
print('1. Mercury')
print('2. Venus')
print('3. Earth')
print('4. Mars')
print('5. Exit the program')
print('Enter your selection.')
choice = int(input(""))
while choice < 1 or choice > 5:
    print('Sorry, that is an invalid selection.')
    print('Enter your choice 1-5.')
    choice = int(input(""))
if choice == 5:
    pass
elif choice == 1:
    print('Mercury')
    print('Average distance from the sun   57.9 million kilometers')
    print('Mass                            3.31 x 10^23 kg')
    print('Surface tempurature             -173 to 430 degrees Celsius')     
elif choice == 2:
    print('Venus')
    print('Average distance from the sun   108.2 million kilometers')
    print('Mass                            4.87 x 10^24 kg')
    print('Surface tempurature             -173 to 430 degrees Celsius')  
elif choice == 3:
    print('Earth')
    print('Average distance from the sun   149.6 million kilometers')
    print('Mass                            35.967 x 10^24 x 10^24 kg')
    print('Surface tempurature             -50 to 50 degrees Celsius') 
elif choice == 4:
    print('Mars')
    print('Average distance from the sun   227.9 million kilometers')
    print('Mass                            .6424 x 10^24 kg')
    print('Surface tempurature             -140 to 20 degrees Celsius')  