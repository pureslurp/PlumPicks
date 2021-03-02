#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 21:37:32 2021

@author: seanraymor
"""
#import libraries
import statistics

#calculate units won or lost
def unitCalc(plum):
    unitData = []
    unitData.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Result = row['Result'].strip()
            Units = float(row['Units'])
            if Line < 0:
                Risk = -1.0
                Win = -100/Line
            else:
                Risk = -1.0
                Win = Line * .01
            if Result == "Win":
                unitData.append(Win * Units)
            elif Result == "Loss":
                unitData.append(Risk * Units)
        except:
            print('unrecognized data')
            unitData = 0
            pass
    return sum(unitData)

def winPerc(plum):
    winRatio = []
    parlayRatio = []
    parlayRatio.clear()
    winRatio.clear()
    try:
        for index, row in plum.iterrows():
            Result = row['Result'].strip()
            Bet = row["Bet"].strip()
            if Result == "Win" and Bet == "Straight":
                winRatio.append(1)
            elif Result == "Loss" and Bet == "Straight":
                winRatio.append(0)
            if Result == "Win" and Bet == "Parlay":
                parlayRatio.append(1)
            elif Result == "Loss" and Bet == "Parlay":
                parlayRatio.append(0)
        if len(winRatio) > 0:
            winP = sum(winRatio)/len(winRatio)
        else:
            winP = "N/A"
        if len(parlayRatio) > 0:
            parlWinP = sum(parlayRatio)/len(parlayRatio)
        else:
            parlWinP = "N/A"
    except:
        print('unrecognizedd data')
        winP = "N/A"
        parlWinP = "N/A"
        pass
    return winP, parlWinP
        
def avgUnit(plum):
    unitAvg = []
    try:
        for index, row in plum.iterrows():
            Units = float(row['Units'])
            unitAvg.append(Units)
        averageUnit = statistics.mean(unitAvg)
    except:
        print("unrecognzied data")
        averageUnit = 0
        pass
    return averageUnit

def strCalc(plum):
    strData = []
    strData.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Result = row['Result'].strip()
            Units = float(row['Units'])
            Bet = row['Bet']
            if Line < 0:
                Risk = -1.0
                Win = -100/Line
            else:
                Risk = -1.0
                Win = Line * .01
            if Result == "Win" and Bet == "Straight":
                strData.append(Win * Units)
            elif Result == "Loss" and "Straight":
                strData.append(Risk * Units)
        except:
            print('unrecognized data')
            strData = 0
            pass
    return sum(strData)

def parlCalc(plum):
    parlData = []
    parlData.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Result = row['Result'].strip()
            Units = float(row['Units'])
            Bet = row['Bet']
            if Line < 0:
                Risk = -1.0
                Win = -100/Line
            else:
                Risk = -1.0
                Win = Line * .01
            if Result == "Win" and Bet == "Parlay":
                parlData.append(Win * Units)
            elif Result == "Loss" and "Parlay":
                parlData.append(Risk * Units)
        except:
            print('unrecognized data')
            parlData = 0
            pass
    return sum(parlData)
