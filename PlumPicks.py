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
#import statistics
import time
from PlumPickFunc import unitCalc, winPerc, strCalc, parlCalc, avgUnit, atRisk, toWin, dayTotal, getDates, findMaxMin, getTotals
#from fancontroller import get_temp, fanOn, fanOff

winColumnPrev = 0
unitColumnPrev = 0

while True:
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
    
    winColumn = dataSheet.col_values(8)
    unitColumn = dataSheet.col_values(7)
    
    #create a DataFrame with all our picks :)
    data = dataSheet.get_all_values()
    headers = data.pop(0)
    dfData = pd.DataFrame(data, columns=headers)
    
    #create a DataFrame with current Stats
    stats = statSheet.get_all_values()
    header = stats.pop(0)
    dfStat = pd.DataFrame(stats, columns=header)
    
    #initialize variables
    plumRideDict = {}
    plumOwnerDict = {}
    plumStatDict = {}
    
    #datetime object containig current date and time
    now = datetime.now()
    #populate plumOwner picks
    for i in plumNames:
        plumOwnerDict[i] = dfData[dfData.Owner == i]
    
    #populate plumRider picks
    for i in plumNames:
        ld = dfData[dfData.Owner != i]
        ld.drop(ld[ld[i].str.strip() != "X"].index, inplace = True)
        plumRideDict[i] = ld
    
    #populate current stats
    for i in plumNames:
        plumStatDict[i] = dfStat[dfStat.Plum == i]
    
    #get current time
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    m = dt_string[:2]
    d = dt_string[4:5]
    y = dt_string[7:10]
    
    #check if updates were made
    if len(list(filter(None,winColumn[1:]))) != winColumnPrev or len(list(filter(None,unitColumn[1:]))) != unitColumnPrev:
        #update sheet
        for i in plumNames:
            for j in range(1,8):
                if statSheet.cell(j,1).value == i:
                    if abs(float(plumStatDict[i]["As Rider (u)"]) - unitCalc(plumRideDict[i])) > 0.1:
                        statSheet.update_cell(j,3, unitCalc(plumRideDict[i]))
                        print("updated {} unit Ride calc".format(i))
                    if abs(float(plumStatDict[i]["As Owner (u)"]) - unitCalc(plumOwnerDict[i])) > 0.1:
                        statSheet.update_cell(j,2, unitCalc(plumOwnerDict[i]))
                        print("updated {} unit Owner calc".format(i))
                    winPercentage = winPerc(plumOwnerDict[i])
                    if abs(float(plumStatDict[i]["In Straight (u)"]) - strCalc(plumOwnerDict[i])) > 0.1:
                        statSheet.update_cell(j,4, strCalc(plumOwnerDict[i]))
                        statSheet.update_cell(j,6, winPercentage[0])
                        print("updated {} straight calc".format(i))
                    if abs(float(plumStatDict[i]["In Parlay (u)"]) - parlCalc(plumOwnerDict[i])) > 0.1:
                        statSheet.update_cell(j,5, parlCalc(plumOwnerDict[i]))
                        statSheet.update_cell(j,7, winPercentage[1])
                        print("updated {} parlay calc".format(i))
                    if float(plumStatDict[i]["At Risk (u)"]) != float((atRisk(plumOwnerDict[i]) + atRisk(plumRideDict[i]))):
                        statSheet.update_cell(j,8, atRisk(plumOwnerDict[i]) + atRisk(plumRideDict[i]))
                        print("updated {} at risk".format(i))
                    if abs(float(plumStatDict[i]["To Win (u)"]) - (toWin(plumOwnerDict[i]) + toWin(plumRideDict[i]))) > 0.1:
                        statSheet.update_cell(j,9, toWin(plumOwnerDict[i]) + toWin(plumRideDict[i]))
                        print("updated {} to win".format(i))
                    if abs(float(plumStatDict[i]["Day Total (u)"]) - (dayTotal(plumOwnerDict[i], m, d) + dayTotal(plumRideDict[i], m , d))) > 0.1:
                        statSheet.update_cell(j,10, dayTotal(plumOwnerDict[i], m, d) + dayTotal(plumRideDict[i], m , d))
                        print("updated {} day total".format(i))
                    if abs(float(plumStatDict[i]["Avg Unit"]) - avgUnit(plumOwnerDict[i])) > 0.01:
                        statSheet.update_cell(j,13, avgUnit(plumOwnerDict[i]))
                        print("updated {} avg unit".format(i))
                    if abs(float(plumStatDict[i]["Week High (u)"]) - findMaxMin(plumOwnerDict[i],plumRideDict[i])[0]) > 0.1:
                        statSheet.update_cell(j,11, findMaxMin(plumOwnerDict[i],plumRideDict[i])[0])
                        print("updated {} week high".format(i))
                    if abs(float(plumStatDict[i]["Week Low (u)"]) - findMaxMin(plumOwnerDict[i],plumRideDict[i])[1]) > 0.1:
                        statSheet.update_cell(j,12, findMaxMin(plumOwnerDict[i],plumRideDict[i])[1])
                        print("updated {} week high".format(i))
        #log time
        print("date and time = ", dt_string)
        statSheet.update_cell(12,2, dt_string)
        statSheet.update_cell(14,2, dt_string)
        x = 0
    else: 
        statSheet.update_cell(14,2, dt_string)
        print('no updates @ {}'.format(dt_string))
    #set prev column length and sleep for 1 min
    winColumnPrev = len(list(filter(None,winColumn[1:])))
    unitColumnPrev = len(list(filter(None,unitColumn[1:])))
    # currTemp = get_temp()
    # if currTemp > 65:
    #     fanOn()
    # else:
    #     fanOff()
    time.sleep(100)
            
        



