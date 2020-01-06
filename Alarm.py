# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 00:22:53 2018

@author: AmatVictoriaCuramIII
"""

#This is an alarm clock, turn up the volume!

import webbrowser
import time

url = 'https://www.youtube.com/watch?v=V2R0K7iX83E'
totalhours = 8 
total = totalhours * 60 * 60
time.sleep(total)
webbrowser.open(url)
