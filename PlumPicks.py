#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 09:21:31 2021

@author: seanraymor
"""
#import libraries
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import statistics


#datetime object containig current date and time
now = datetime.now()

#establish connection to google sheets
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
client = gspread.authorize(creds)

#assign data sheet vs. stat sheet
statSheet = client.open("Plum Picks").worksheet("Stats")
dataSheet = client.open("Plum Picks").sheet1

#grab our names and assign to array of strings
Plums = statSheet.col_values(1)
plumNames = Plums[1:]

#create a DataFrame with all our picks :)
data = dataSheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)

#initialize variables
plumRideDict = {}
plumOwnerDict = {}

#populate plumOwner picks
for i in plumNames:
    plumOwnerDict[i] = df[df.Owner == i]

#populate plumRider picks
for i in plumNames:
    ld = df[df.Owner != i]
    ld.drop(ld[ld[i].str.strip() != "X"].index, inplace = True)
    plumRideDict[i] = ld

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
        winP = sum(winRatio)/len(winRatio)
        parlWinP = sum(parlayRatio)/len(parlayRatio)
    except:
        print('unrecognized data')
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


#update sheet
for i in plumNames:
    for j in range(1,8):
        if statSheet.cell(j,1).value == i:
            statSheet.update_cell(j,3, unitCalc(plumRideDict[i]))
            statSheet.update_cell(j,2, unitCalc(plumOwnerDict[i]))
            winPercentage = winPerc(plumOwnerDict[i])
            statSheet.update_cell(j,4, strCalc(plumOwnerDict[i]))
            statSheet.update_cell(j,5, parlCalc(plumOwnerDict[i]))
            statSheet.update_cell(j,6, winPercentage[0])
            statSheet.update_cell(j,7, winPercentage[1])
            statSheet.update_cell(j,8, avgUnit(plumOwnerDict[i]))
            
        
#log time
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("date and time = ", dt_string)

statSheet.update_cell(12,2, dt_string)



