#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 13:37:36 2021

@author: seanraymor
"""

import subprocess
import time

from gpiozero import OutputDevice

ON_THRESHOLD = 65
OFF_THRESHOLD = 55
SLEEP_INTERVAL = 5
GPIO_PIN = 17

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except:
        raise RuntimeError('Could not parse temperature output')
         
fan = OutputDevice(GPIO_PIN)

def fan(temp):
    if temp > ON_THRESHOLD and not fan.value:
        fan.on()
        
    elif fan.value and temp < OFF_THRESHOLD:
        fan.off()
        
    time.sleep(SLEEP_INTERVAL)