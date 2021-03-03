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
            pass
    if not unitData:
        unitData = [0,0]
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
    averageUnit = 0
    for index, row in plum.iterrows():
        try:
            Units = float(row['Units'])
            unitAvg.append(Units)
        except:
            pass
    averageUnit = statistics.mean(unitAvg)
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
            elif Result == "Loss" and Bet == "Straight":
                strData.append(Risk * Units)
        except:
            print('unrecognized data')
            pass
    if not strData:
            strData = [0,0]
    return sum(strData)

def parlCalc(plum):
    parlData = []
    parlData.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Result = row['Result'].strip()
            Units = float(row['Units'])
            Bet = row['Bet'].strip()
            if Line < 0:
                Risk = -1.0
                Win = -100/Line
            else:
                Risk = -1.0
                Win = Line * .01
            if Result == "Win" and Bet == "Parlay":
                parlData.append(Win * Units)
            elif Result == "Loss" and Bet == "Parlay":
                parlData.append(Risk * Units)
        except:
            print('unrecognized data')
            pass
    if not parlData:
        parlData = [0,0]
    return sum(parlData)

def atRisk(plum):
    atRiskArray = []
    atRiskArray.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Units = float(row['Units'])
            if row['Result'] == "":
                if Line < 0:
                    Risk = -1.0
                    #Win = -100/Line
                else:
                    Risk = -1.0
                    #Win = Line * .01
                atRiskArray.append(Risk * Units)
        except:
            print('unrecognized data')
            pass
    if not atRiskArray:
        atRiskArray = [0,0]
    return sum(atRiskArray)
                
    
def toWin(plum):
    toWinArray = []
    toWinArray.clear()
    for index, row in plum.iterrows():
        try:
            Line = int(row['Line'])
            Units = float(row['Units'])
            if row['Result'] == "":
                if Line < 0:
                    #Risk = -1.0
                    Win = -100/Line
                else:
                    #Risk = -1.0
                    Win = Line * .01
                toWinArray.append(Win * Units)
        except:
            print('unrecognized data')
            pass
    if not toWinArray:
        toWinArray = [0,0]
    return sum(toWinArray)
    
    
    
    
    
