#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 13:37:36 2021

@author: seanraymor
"""

import subprocess

from gpiozero import OutputDevice

GPIO_PIN = 17

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except:
        raise RuntimeError('Could not parse temperature output')
         
fan = OutputDevice(GPIO_PIN)

def fanOn():
    fan.on()
    
def fanOff():
    if fan.value == 1:
        fan.off()