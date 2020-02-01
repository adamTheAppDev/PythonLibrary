# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is an alarm clock, turn up the volume!

#Import modules
import webbrowser
import time

#Input URL
url = 'https://www.youtube.com/watch?v=V2R0K7iX83E'
#Input hours until alarm
totalhours = 8 
#Calculate seconds until alarm
total = totalhours * 60 * 60
time.sleep(total)
#Open URL - turn up volume!
webbrowser.open(url)
