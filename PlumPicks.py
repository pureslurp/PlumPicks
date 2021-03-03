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
from PlumPickFunc import unitCalc, winPerc, strCalc, parlCalc, avgUnit

winColumnPrev = 0

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
    
    #create a DataFrame with all our picks :)
    data = dataSheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    
    #initialize variables
    plumRideDict = {}
    plumOwnerDict = {}
    #datetime object containig current date and time
    now = datetime.now()
    #populate plumOwner picks
    for i in plumNames:
        plumOwnerDict[i] = df[df.Owner == i]
    
    #populate plumRider picks
    for i in plumNames:
        ld = df[df.Owner != i]
        ld.drop(ld[ld[i].str.strip() != "X"].index, inplace = True)
        plumRideDict[i] = ld
    
    #get current time
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    
    #check if updates were made
    if len(list(filter(None,winColumn[1:]))) != winColumnPrev:
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
        print("date and time = ", dt_string)
        statSheet.update_cell(12,2, dt_string)
        x = 0
    else: 
        print('no updates @ {}'.format(dt_string))
    #set prev column length and sleep for 1 min
    winColumnPrev = len(list(filter(None,winColumn[1:])))
    time.sleep(60)
            
        




