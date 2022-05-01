"""Models for matrixmendations - Seperate for Mood vs other factors"""
from flask import Flask, request
from flask_jsonpify import jsonify 
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
#from resources  import core 
import math 
import random
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import csv
from datetime import datetime, date, timedelta
import tensorflow
# import gym
# import keras
import torch
import torch.nn as nn
import tez
from sklearn import model_selection, metrics, linear_model, preprocessing
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display
import operator
import urllib #to post to php
from sqlalchemy import create_engine
import pymysql
import mysql.connector
import schedule
import time
import recommendW as recommendW
import recommendS as recommendS
import recommendM as recommendM

# def daily():
#establishing the connection
conn = mysql.connector.connect(
user='root', host='127.0.0.1', database='mindme')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Retrieving single row
sql = "SELECT * from pyth WHERE id=1"

#Executing the query
cursor.execute(sql)

#Fetching 1st row from the table
data = cursor.fetchone()

###CHECK THE RIGHT USER 

user = data[0]


"""Cleaning and Importing Data """
activitydf = pd.read_csv('../csv/activity.csv')
sleepdf = pd.read_csv('../csv/sleep.csv')
datadf = pd.read_csv('../csv/data.csv')
predactdf = pd.read_csv('../csv/predact.csv')
predsledf = pd.read_csv('../csv/predsle.csv')


sleepdf['day'] = pd.to_datetime(sleepdf['End']).dt.date #day finished sleeping
sleepdf['starttime'] = pd.to_datetime(sleepdf['Start']).dt.time #time began sleeping
sleepdf.rename(columns={'Sleep quality': 'sleepqual','Time in bed': 'tib','Wake up': 'wakeup','Sleep Notes': 'sleepnotes', 'Heart rate':'heartrate', 'Activity (steps)':'steps'}, inplace=True)
sleepdf['sleepqual'] = sleepdf['sleepqual'].replace("%", "", regex=True)
sleepdf['sleepqual'] = sleepdf['sleepqual'].astype(int)

activitydf.rename(columns={'Minutes Sedentary': 'minsed', 'Steps': 'steps', 'Day': 'day'}, inplace=True)
activitydf['steps'] = activitydf['steps'].replace(",", "", regex=True)
activitydf['steps'] = activitydf['steps'].astype(float)
activitydf['day'] = activitydf['day'].replace("-", "", regex=True)
activitydf['day'] = pd.to_datetime(activitydf['day'], format='%Y%m%d')


matrix = pd.read_csv("../csv/matrix1.csv", index_col=0 ) #The NAN data given 0 - where users havent seen the matrixmendation yet
recoms = pd.read_csv("../csv/recoms.csv")
matrix = matrix.pivot_table(index='user', columns='recom', values='rating')
matrix = matrix.fillna(0)

msgm = ''
msgw = ''
msgsl = ''


points7 = 0 #points count for the user;s week
points1 = 0#points count for the user;s month
points3 = 0#points count for the user;s 3 months
count7 = 0 # count of how many times user was at best threshold for each step and sleep of that week
count1 = 0  # count of how many times user was at best threshold for each step and sleep of that month
count3 = 0 # count of how many times user was at best threshold for each step and sleep of those 3 months

"""Creating Linear Regression Models"""

"""ASSUMPTIONS: DATA ENTERED DAILY """

"""PREDICTING DAY VS STEPS BASED ON PAST """
""" This function steps creates graphs of the users step count for the past week, month and 3 months.
    This function creates prediction of the users next weeks, months or 3 months step count and average step count
    The function then produces a message or matrixmendation based on their progress the past week, and if its below / above matrixmended threshold 
"""

# stepscoef = reg.coef_ #coeeficient of graph
# stepsinter = reg.intercept_ #interpcept

# countp = 0 #
# prevlen7 = 7 #using this as a count that can remember up until how many days the prediction needs to be counted for 
# prevlen1 = 28
# prevlen3 = 77
cols = ['predday', 'predstep'] #headers for temporary prediction dataframe
predstep = [] #array to contain all the predicted steps of the week week 
# count = 0 #place to insert data
# avgstep7 = 0 #average steps of this week
# avgstep1 = 0#average steps of this month
# avgstep3 = 0#average steps of this 3 months



if len(activitydf)%84 == 0: #3 months  0 - 77-84, 85-(161-168) 
    """CREATING DAY VS STEPS BASED ON PAST 3 MONTHS """
    xticks = activitydf.day[len(activitydf)-84:len(activitydf)]
    day = [k for k in range(len(activitydf.day)-84,len(activitydf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, activitydf.steps[len(activitydf)-84:len(activitydf)]) 
    plt.title('Your Steps These 3 Months')
    plt.xticks(day, xticks)
    plt.savefig('../src/assets/img/activity3.png')


    avgstep3 = activitydf.steps[len(activitydf)-84:len(activitydf)] / 84 
    if avgstep3 < (sum(activitydf.steps[len(activitydf)-84:len(activitydf)]) / 84) :
        print("WOW! Doing well. Your average steps of these 3 months are higher than last 3 months. Keep it up!")
    if avgstep3 >=  504000:
            count3 += 1 #adds to count that user is above threshold for points
    elif 336000 <= avgstep3 < 504000: 
        stepmatrix = ''
    else:
        stepmatrix = ''
    

    ps = []
    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1), activitydf.steps[len(activitydf)-84:len(activitydf)])#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints
    
    """CREATING DAY VS STEPS BASED ON PAST 3 MONTHS """
    for i in range(prevlen3, len(activitydf)+7): #0-6 activity, 7-13 
        preddays = activitydf.loc[i-7, 'day'] + timedelta(days=7) #gets the next 7 days one by one
        predsteps = reg.predict(np.array([[i]])) #predicts steps for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predstep += predsteps # add pred steps for that day in DB
        ps.append([preddays, predsteps])    
        #ps = pd.DataFrame([[preddays, predsteps]], columns =['predday', 'predstep']) # puts the next predicted day up to 7 days steps in df
        #ps.to_csv('../csv/pred.csv', index=count) #put day and step in DB
        #xticks += preddays #temporary
        count3 += 1
    preddf['predstep'] = preddf['predstep'].replace("[]", "", regex=True)
    preddf = pd.DataFrame(ps, columns=cols)
    # xticks = preddf.predday[len(preddf)-84:len(preddf)]
    # preddaysnum = [k for k in range(prevlen3, len(preddf.predday))] #must convert x axis to float therefore last previous day of recording
    # plt.scatter(preddaysnum, preddf.predstep) #creates graph of next week prediction
    # plt.xticks(preddaysnum, xticks)
    # plt.title('Next 3 Months Predicted Steps')
    # plt.show()
    avgpredstep = sum(predstep) / 84 #find average of the predicted step count 
    if avgpredstep >= 6400:
        count3 += 1 #keep a count of how many 7 days passed
    prevlen3 = len(activitydf)-7 # keep track of last predicted 28 days
elif len(activitydf)%28 == 0: #1 month 0 - 20-27, 28-(49-56) 
    """CREATING DAY VS STEPS BASED ON PAST MONTH """
    xticks = activitydf.day[len(activitydf)-28:len(activitydf)]
    day = [k for k in range(len(activitydf.day)-28, len(activitydf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, activitydf.steps[len(activitydf)-28:len(activitydf)]) 
    plt.title('Your Steps This Month')
    plt.xticks(day, xticks)
    plt.savefig('../src/assets/img/activity1.png')
    plt.show()

    avgstep1 = sum(activitydf.steps[len(activitydf)-28:len(activitydf)]) / 28
    if avgstep1 < (sum(activitydf.steps[len(activitydf)-28:len(activitydf)]) / 28) :
        print("This is great!! Your average steps of this month are higher than the other month. Keep it up!")
    if avgstep1 >=  168000: #5 x a week 8000 steps
            count1 += 1 #adds to count that user is above threshold for points
    elif 112000 <= avgstep1 < 168000:
        stepmatrix = ''
    else:
        stepmatrix = ''

    ps = []

    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1),  activitydf.steps[len(activitydf.day)-28:len(activitydf.day)])#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints
    
    """PREDICTING DAY VS STEPS BASED ON PAST MONTH """
    for i in range(prevlen1, len(activitydf)+28): 
        preddays = activitydf.loc[i-28, 'day'] + timedelta(days=28) #gets the prev 7 days one by one (21-28, etc)
        predsteps = reg.predict(np.array([[i]])) #predicts steps for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predstep += predsteps # add pred steps for that day in DB
        ps.append([preddays, predsteps])
    predactdf['predstep'] = predactdf['predstep'].replace("\[]/", "", regex=True)
    predactdf = pd.DataFrame(ps, columns=cols) #add all the predicted data to the df
    predactdf.to_csv('../csv/predact.csv', mode='a', index=False, header=False) #save the data in the prediction dataframe CSV
    # xticks = preddf.predday[len(preddf)-28:len(preddf)]
    # preddaysnum = [k for k in range(prevlen1, len(preddf.predday))] #must convert x axis to float therefore 1 is day 1 of recording
    # display(preddf)
    # plt.scatter(preddaysnum, preddf.predstep) #creates graph of next week prediction
    # plt.xticks(preddaysnum, xticks)
    # plt.title('Next Months Predicted Steps')
    # plt.show()
    avgpredstep = np.sum(predactdf.predstep[len(predactdf)-28:len(predactdf)]) /28 #find average of the predicted step count 

    """CALCULATING PREDICTED AVERAGE STEPS  """
    if avgpredstep >=  168000:
        print("Your predicted steps for next week is" + str(avgpredstep) +". Keep it up!")
    elif 112000 <= avgpredstep < 168000:
        print("Your predicted steps for next week is" + str(avgpredstep) +". What can we change?") 
    else:
        print("Your predicted steps for next week is" + str(avgpredstep) +". Let's see how we can improve this.") 

    # matrixdf.to_csv('../csv/matrix.csv', mode='a', index=False, header=False)
    
    ##post data to matrix csv
    prevlen1 = len(activitydf)-7 # keep track of last predicted 28 days
elif len(activitydf)%7 == 0: #7 days #activitydf['day'].between(int(prevlen), activitydf.shape[1]


    """CREATING DAY VS STEPS GRAPH BASED ON PAST WEEK """
    xticks = activitydf.day[len(activitydf)-7:len(activitydf)]
    day = [k for k in range(len(activitydf.day)-7,len(activitydf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.plot(day, activitydf.steps[len(activitydf)-7:len(activitydf)]) 
    plt.title('Your Steps This Week')
    plt.xticks(day, xticks)
    plt.xticks(rotation='vertical')
    plt.savefig('C://xampp/htdocs/project/mindme/src/assets/img/activity7.png') ##STORE GRAPH AS IMG
    plt.show()


    "USE AVERAGE STEPS TO ADD SCORE TO matrix RECOMMENDATION PROVIDED"
    val = ((sum(activitydf.steps[len(activitydf)-7:len(activitydf)]) / 7) - data[12])
    if val >= 2000:
        v = 5
    elif 0 < val < 2000:
        v = 4
    elif val == 0:
        v = 3 
    elif -500 < val < 0:
        v = 2
    else:
        v = 1

    # #MUST START WITH THIS RECOMMENDATION ALREADY PROVIDED AND 2 weeks data
    # sql = '''SELECT * from recommendations'''
    # cursor.execute(sql)
    # data2 = cursor.fetchone()

    # stepmatrix = data2[0] #gets the older recommendation for that week
    # matrix.loc[user,stepmatrix] = v #puts the rating for that recommendation
    # matrix.to_csv('../csv/matrix1.csv', mode='w', index=False, header=False) #post in DB

    avgstep7 = (sum(activitydf.steps[len(activitydf)-7:len(activitydf)]) / 7)

    "CALCULATING AVERAGE STEPS OF THE WEEK - PRODUCING A MESSAGE IF BETETR THAN PREVIOUS, GIVING MESSAGE AND matrixMENDATIONS IF BELOW CERTAIN THRESHOLDS"
    
    if data[12] < avgstep7 :
        msgw = "This is great!! Your average steps of this month are higher than the other month. Keep it up!"
    if avgstep7 >=  5714: #5 x a week 8000 steps
        count7 += 1 #adds to count that user is above threshold for points - post to php
    elif 3428 <= avgstep7 < 5714:
        stepmatrix = recommendW.recom
    else:
        stepmatrix = recommendW.recom

    sql = "UPDATE pyth SET avgstep7 = '%s' WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (avgstep7, user)
    cursor.execute(sql, var)
    conn.commit()

    
    ps = [] #2D array for prediction of next weeks steps 
    "CREATING PREDICTION MODEL "
    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1), activitydf.steps[len(activitydf)-7:len(activitydf)])#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints

    """PREDICTING DAY VS STEPS BASED ON PAST WEEK """
    for i in range(data[8], len(activitydf)+7): #0-6 activity, 7-13 
        preddays = activitydf.loc[i-7, 'day'] + timedelta(days=7) #gets the next 7 days one by one
        predsteps = reg.predict(np.array([[i-7]])) #predicts steps for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predstep += predsteps # add pred steps for that day in DB
        ps.append([preddays, predsteps]) #add the daat to an array of data
    predactdf['predstep'] = predactdf['predstep'].replace("s/[\[\]']+/g", "", regex=True)
    predactdf = pd.DataFrame(ps, columns=cols) #add all the predicted data to the df
    predactdf.to_csv('../csv/predact.csv', mode='a', index=False, header=False) #save the data in the prediction dataframe CSV
    # xticks = predactdf.predday[len(predactdf)-7:len(predactdf)] #x axis for dataframe using all the days
    # preddaysnum = [k for k in range(prevlen7-7, len(predactdf.predday))] #must convert x axis to float therefore 1 is day 1 of recording
    # plt.scatter(preddaysnum, predactdf.predstep[len(predactdf)-7:len(predactdf)]) #creates graph of next week prediction
    # plt.xticks(preddaysnum, xticks)
    # plt.title('Next Weeks Predicted Steps')
    # plt.show()
    avgpredstep = np.sum(predactdf.predstep[len(predactdf)-7:len(predactdf)]) /7 #find average of the predicted step count 

    """CALCULATING PREDICTED AVERAGE STEPS  """
    if avgpredstep >=  5714:
        predmsgw = "Your predicted steps for next week is" + str(avgpredstep) +". Keep it up!"
    elif 3428 <= avgpredstep < 5714:
        predmsgw = "Your predicted steps for next week is" + str(avgpredstep) +". What can we change?"
    else:
        predmsgw = "Your predicted steps for next week is" + str(avgpredstep) +". Let's see how we can improve this."
    
    prevlen7 = len(activitydf) # keep track of last predicted 7 days POST TO MYSQL
    sql = "UPDATE pyth SET prevlen7 = '%s' WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (prevlen7, user)
    cursor.execute(sql, var)
    conn.commit()

    sql = "UPDATE pyth SET msgw = %s, predmsgw=%s WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (msgw, predmsgw, user)
    cursor.execute(sql, var)
    conn.commit()


"""CREATING GRAPH MOOD VS DAYS BASED"""

""" This function steps creates graphs of the users mood for the past week, month and 3 months. 
"""
avgmood7 = 0 #looking at the amount of :) and :( a user has over a time period and producing a message and matrix based on it
avgmood1 = 0
avgmood3 = 0 
countmood7 = 0
countmood1 = 0
countmood3 = 0


mooddf = "SELECT * FROM mood WHERE id=1" #gets most recent 7 days of moods
cursor = conn.cursor(dictionary=True)
cursor.execute(mooddf)
result = cursor.fetchall()

# # def dmgraph():

"""DAY VS MOOD""" 
if len(datadf)%84 == 0: #3 months 
    xticks = datadf.day[len(datadf)-84:len(datadf)]
    day = [k for k in range(len(datadf)-84,len(datadf))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, datadf.mood[len(datadf)-84:len(datadf)]) 
    plt.title('Your Mood These 3 months')
    plt.xticks(day, xticks)
    plt.savefig('../src/assets/img/mood3.png')
    plt.show()

    for i in range(len(datadf)-84,len(datadf)):
         if datadf.mood[i] == 1:
            avgmood7 += datadf.mood[i]

    if avgmood3 >= 63:
        if countmood3 > 1:
            print("You're past three months have been amazing! Your past" + countmood3 + "months have been good so far!")
        else:
            print("You're past three months have been amazing!!")
        countmood3 += 1
    if 42 <= avgmood3 < 63:
        print("Hope you're ok! Let's unpack these 3 months.")
        moodmatrix = ''
        countmood3 = 0
    elif avgmood3 < 42:
        print("Let's see if we can help improve your next 3 months.")
        moodmatrix = ''
        countmood3 = 0
    count3 += 1
elif len(datadf)%28 == 0: #1 month
    xticks = datadf.day[len(datadf)-28:len(datadf)]
    day = [k for k in range(len(datadf)-28,len(datadf))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, datadf.mood[len(datadf)-7:len(datadf)]) 
    plt.title('Your Mood This Month')
    plt.xticks(day, xticks)
    plt.savefig('../src/assets/img/mood1.png')
    plt.show()

    for i in range(len(datadf)-28,len(datadf)):
        if datadf.mood[i] == 1:
            avgmood7 += datadf.mood[i]

    if avgmood1 >= 21:
        if countmood1 > 1:
            print("I'm glad your month went well! Your past" + countmood1 + "weeks have been good so far!")
        else:
            print("I'm glad your month went well!")
        countmood1 += 1
    if 14 <= avgmood1 < 21:
        print("Hope you're ok! Let's unpack this month.")
        moodmatrix = ''
        countmood1 = 0
    elif avgmood7 < 14:
        print("Let's see if we can help improve your next month.")
        moodmatrix = ''
        countmood1 = 0
    count1 += 1

elif len(result)%7  == 0: #7 days #activitydf['day'].between(int(prevlen), activitydf.shape[1]
    
    
    # xticks = datadf.day[len(datadf)-7:len(datadf)]
    # day = [k for k in range(len(datadf)-7,len(datadf))] #must convert x axis to float therefore 1 is day 1 of recording
    # plt.plot(day, datadf.mood[len(datadf)-7:len(datadf)]) 
    
    mooddf = "SELECT * FROM (SELECT * FROM mood WHERE id=1 ORDER BY timestamp DESC LIMIT 7) T1 ORDER BY timestamp " #gets most recent 7 days of moods
    cursor = conn.cursor(dictionary=True)
    cursor.execute(mooddf)
    result = cursor.fetchall()

    mood = []
    xticks = []
    
    for i in range(len(result)-7, len(result)):
        xticks.append(result[i].get('timestamp'))
        mood.append(result[i].get('emot'))
    #plt.scatter(day, mood) 
    day = [k for k in range(len(result)-7,len(result))]
    plt.plot(day, mood) 

    plt.title('Your Mood This Week')
    plt.xticks(day, xticks)
    plt.xticks(rotation='vertical')
    plt.savefig('C://xampp/htdocs/project/mindme/src/assets/img/mood7.png') ##STORE GRAPH AS IMG
    plt.show()

    "USE AVERAGE MOOD TO ADD SCORE TO matrix RECOMMENDATION PROVIDED"
    val = (((sum(mood)) / 7) - data[12])
    if val >= 2:
        v = 5
    elif 0 < val < 2:
        v = 4
    elif val == 0:
        v = 3 
    elif 2 < val < 0:
        v = 2
    else:
        v = 1

    # #MUST START WITH THIS RECOMMENDATION ALREADY PROVIDED AND 2 weeks data
    # sql = '''SELECT * from recommendations'''
    # cursor.execute(sql)
    # data2 = cursor.fetchone()

    # stepmatrix = data2[] #gets the older recommendation for that week
    # matrix.loc[user,stepmatrix] = v #puts the rating for that recommendation
    # matrix.to_csv('../csv/matrix1.csv', mode='w', index=False, header=False) #post in DB

    #adds the 1 to mood rating if its 1
    for i in range(len(result)-7,len(result)):
        if mood[i] == 1:
            avgmood7 += 1

    if avgmood7 >= 5:
        if data[12] > 1:
            msgm = "I'm glad your week went well! Your past" + data[12] + "weeks have been good so far!"
        else:
            msgm = "I'm glad your week went well!"
        countmood7 += 1
    if 2 <= avgmood7 < 5:
        msgm = "Hope you're ok! Let's unpack."
        moodmatrix = recommendM.recom
        countmood7 = 0
    elif avgmood7 < 2:
        msgm = "Let's see if we can help improve your next week."
        moodmatrix = recommendM.recom
        countmood7 = 0

    sql = "UPDATE pyth SET avgmood7= '%s', countmood7 = '%s' WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (avgmood7, countmood7, user)
    cursor.execute(sql, var)
    conn.commit()

    sql = "UPDATE pyth SET msgm=%s WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (msgm, user)
    cursor.execute(sql, var)
    conn.commit()

"""SLEEP QUALITY VS BEGINTIME(TIME)"""
cols = ['predday', 'predsle'] #headers for temporary prediction dataframe
predqual = []
slematrix = '' #matrixmendation prodived to user
# count = 0 #place to insert data
# avgsle7 = 0 
# avgsle1 = 0
# avgsle3 = 0



if len(sleepdf)%84 == 0: #3 months  0 - 77-84, 85-(161-168) 
    """CREATING DAY VS Sleep BASED ON PAST 3 MONTHS """
    xticks = sleepdf.day[len(sleepdf)-84:len(sleepdf)]
    day = [k for k in range(len(sleepdf.day)-84, len(sleepdf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, sleepdf.sleepqual) 
    plt.title('Your Sleep These 3 Months')
    plt.savefig('../src/assets/img/sleep3.png')
    plt.xticks(day, xticks)
    if avgsle3 < (sum(sleepdf.sleepqual[len(sleepdf)-84:len(sleepdf)]) / 84) :
        print("WOW! Doing well. Your average Sleep of these 3 months are higher than last 3 months. Keep it up!")
    else:
        stepmatrix = '' 
    avgsle3 = sleepdf.sleepqual[len(sleepdf)-84:len(sleepdf)] / 84 
    ps = []
    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1), sleepdf.sleepqual)#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints
    
    """CREATING DAY VS Sleep BASED ON PAST 3 MONTHS """
    for i in range(prevlen3, len(sleepdf)+7): #0-6 activity, 7-13 
        preddays = sleepdf.loc[i-7, 'day'] + timedelta(days=7) #gets the next 7 days one by one
        predquals = reg.predict(np.array([[i]])) #predicts Sleep for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predqual += predquals # add pred Sleep for that day in DB
        ps.append([preddays, predquals])
        #ps = pd.DataFrame([[preddays, predSleep]], columns =['predday', 'predsle']) # puts the next predicted day up to 7 days Sleep in df
        #ps.to_csv('../csv/pred.csv', index=count) #put day and step in DB
        #xticks += preddays #temporary
        count3 += 1
    preddf['predsle'] = preddf['predsle'].replace("[]", "", regex=True)
    preddf = pd.DataFrame(ps, columns=cols)
    xticks = preddf.predday[len(preddf)-84:len(preddf)]
    preddaysnum = [k for k in range(prevlen3, len(preddf.predday))] #must convert x axis to float therefore last previous day of recording
    plt.scatter(preddaysnum, preddf.predsle) #creates graph of next week prediction
    plt.xticks(preddaysnum, xticks)
    plt.title('Next 3 Months Predicted Sleep')
    plt.show()
    avgpredsle = sum(predsle) / 84 #find average of the predicted step count 
    if avgpredsle >= 6400:
        count3 += 1 #keep a count of how many 7 days passed
    prevlen3 = len(sleepdf)-7 # keep track of last predicted 28 days
elif len(sleepdf)%28 == 0: #1 month 0 - 20-27, 28-(49-56) 
    """CREATING DAY VS Sleep BASED ON PAST MONTH """
    xticks = sleepdf.day[len(sleepdf)-28:len(sleepdf)]
    day = [k for k in range(len(sleepdf.day)-28, len(sleepdf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.scatter(day, sleepdf.sleepqual) 
    plt.title('Your Sleep This Month')
    plt.savefig('../src/assets/img/sleep1.png')
    plt.xticks(day, xticks)
    if avgsle1 < (sum(sleepdf.sleepqual[len(sleepdf)-28:len(sleepdf)]) / 28) :
        print("This is great!! Your average Sleep of this month are higher than the other month. Keep it up!")
    else:
        stepmatrix = ''
    avgsle1 = sleepdf.sleepqual[len(sleepdf)-28:len(sleepdf)] / 28
    ps = []
    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1), sleepdf.sleepqual)#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints
    
    """PREDICTING DAY VS Sleep BASED ON PAST MONTH """
    for i in range(prevlen1, len(sleepdf)+7): 
        preddays = sleepdf.loc[i-7, 'day'] + timedelta(days=7) #gets the prev 7 days one by one (21-28, etc)
        predquals = reg.predict(np.array([[i]])) #predicts Sleep for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predqual += predquals # add pred Sleep for that day in DB
        ps.append([preddays, predquals])
        #ps = pd.DataFrame([[preddays, predSleep]], columns =['predday', 'predsle']) # puts the next predicted day up to 7 days Sleep in df
        #ps.to_csv('../csv/pred.csv', index=count) #put day and step in DB
        #xticks += preddays #temporary
        count1 += 1
    preddf['predsle'] = preddf['predsle'].replace("[]", "", regex=True)
    preddf = pd.DataFrame(ps, columns=cols)
    xticks = preddf.predday[len(preddf)-28:len(preddf)]
    preddaysnum = [k for k in range(prevlen1, len(preddf.predday))] #must convert x axis to float therefore 1 is day 1 of recording
    display(preddf)
    plt.scatter(preddaysnum, preddf.predsle) #creates graph of next week prediction
    plt.xticks(preddaysnum, xticks)
    plt.title('Next Months Predicted Sleep')
    plt.show()



    avgpredsle = sum(predsle) / 28 #find average of the predicted step count 
    if avgpredsle >=  6000:
        count1 += 1
    prevlen1 = len(sleepdf)-7 # keep track of last predicted 28 days
elif len(sleepdf)%7 == 0: #7 days #sleepdf['day'].between(int(prevlen), sleepdf.shape[1]

    """CREATING SLEEP QUALITY VS DAY BASED ON PAST WEEK """
    xticks = sleepdf.day[len(sleepdf)-7:len(sleepdf)]
    day = [k for k in range(len(sleepdf.day)-7,len(sleepdf.day))] #must convert x axis to float therefore 1 is day 1 of recording
    plt.plot(day, sleepdf.sleepqual[len(sleepdf)-7:len(sleepdf)]) 
    plt.title('Your Sleep This Week')
    plt.xticks(day, xticks)
    plt.xticks(rotation='vertical')
    plt.savefig('C://xampp/htdocs/project/mindme/src/assets/img/sleep7.png')
    plt.show()

    val = (sum(sleepdf.sleepqual[len(sleepdf)-7:len(sleepdf)]) / 7 - data[18])
    if val >= 10:
        v = 5
    elif 0 < val <= 10:
        v = 4
    elif val == 0:
        v = 3 
    elif val <= -5:
        v = 1
    else:
        v = 1      
    
    # #MUST START WITH THIS RECOMMENDATION ALREADY PROVIDED AND 2 weeks data
    # sql = '''SELECT * from recommendations where recom'''
    # cursor.execute(sql)
    # data2 = cursor.fetchone()

    # stepmatrix = data2[] #gets the older recommendation for that week
    # matrix.loc[user,stepmatrix] = v #puts the rating for that recommendation
    # matrix.to_csv('../csv/matrix1.csv', mode='w', index=False, header=False) #post in DB

    
    avgsle7 = sum(sleepdf.sleepqual[len(sleepdf)-7:len(sleepdf)]) / 7
    
    if data[18] < avgsle7 :
        msgsl = "This is great!! Your average sleep of this week are higher than the last week. Keep it up!"
    if data[18] >= 85:
        count7 += 1 
    elif 70 <= avgsle7 < 85:
        slematrix = recommendS.recom
        print(slematrix)
    else:
        slematrix = recommendS.recom
        print(slematrix)

    sql = "UPDATE pyth SET avgsle7 = '%s' WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (avgsle7, user)
    cursor.execute(sql, var)
    conn.commit()

    ps = []
    reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
    reg.fit(np.array(day).reshape(-1, 1), sleepdf.sleepqual[len(sleepdf.day)-7:len(sleepdf.day)])#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints

    """PREDICTING DAY VS Sleep BASED ON PAST WEEK """
    for i in range(data[8], len(sleepdf)+7): #0-6 activity, 7-13 
        preddays = sleepdf.loc[i-7, 'day'] + timedelta(days=7) #gets the next 7 days one by one
        predquals = reg.predict(np.array([[i-7]])) #predicts Sleep for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
        predqual += predquals # add pred Sleep for that day in DB
        ps.append([preddays, predquals]) #add the daat to an array of data
        #standdev = sqrt((sleepdf.mean())/7)
        #sleepdf.loc[i-7, 'starttime'].dt.total_seconds()
    predsledf = pd.DataFrame(ps, columns=cols) #add all the predicted data to the df
    predsledf['predsle'] = predsledf['predsle'].replace("/[\[\]']+/g", "", regex=True)
    predsledf.to_csv('../csv/predsle.csv', mode='a', index=False, header=False) #save the data in the prediction dataframe CSV
    # xticks = predsledf.predday[len(predsledf)-7:len(predsledf)] #x axis for dataframe using all the days
    # preddaysnum = [k for k in range(prevlen7-7, len(predsledf.predday))] #must convert x axis to float therefore 1 is day 1 of recording
    # plt.scatter(preddaysnum, predsledf.predsle[len(predsledf)-7:len(predsledf)]) #creates graph of next week prediction
    # plt.xticks(preddaysnum, xticks)
    # plt.title('Next Weeks Predicted Sleep')
    # plt.show()
    avgpredsle = np.sum(predsledf.predsle[len(predsledf)-7:len(predsledf)]) /7#find average of the predicted step count 
    #print(sleepdf['starttime'].dt.total_seconds().std())
    """CALCULATING PREDICTED AVERAGE QUALITY AND USING STARTTIME TO PRODUCE matrix."""
    if avgpredsle >= 85:
        predmsgs = "Your predicted sleep quality for next week is" + str(avgpredsle) +". Keep it up!"
        count7 += 1 
    else:
        predmsgs = "Your predicted sleep quality for next week is" + str(avgpredsle) +". What can we change?"
        #if standard dev :
        #   sleepmatrix = ''
        ##check if standard devation of start time fluctates 


    prevlen7 = len(sleepdf) # keep track of last predicted 7 days
    sql = "UPDATE pyth SET prevlen7 = '%s' WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (prevlen7, user)
    cursor.execute(sql, var)
    conn.commit()

    sql = "UPDATE pyth SET msgsl= %s, predmsgs=%s WHERE id=%s" #post the avgsteps to db
    # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
    var = (msgsl, predmsgs, user)
    cursor.execute(sql, var)
    conn.commit()

x = 0
z = 0 

"""points count"""
if count1|count3|count7 != 0:
    if count3 >= 4:
        points3 += 100
        x = points3
        sqlquery = "UPDATE pyth SET points3 = '%s', points = points + 100 where id = %s"
    elif count3 >= 2:
        points3 += 50
        sqlquery = "UPDATE pyth SET points3= '%s', points = points + 50 where id = %s"
        x = points3
    elif count1 >= 2:
        points1 += 25
        sqlquery = "UPDATE pyth SET points1= '%s',points = points + 25 where id = %s"
        x = points1
    elif count7 >= 1:
        points7 += 5
        sqlquery = "UPDATE pyth SET points7= '%s', points = points + 5 where id = %s"
        x = points7

    var = (x, user)
    cursor.execute(sqlquery, var)
    conn.commit()
    #Closing the connection
    conn.close()
    

#schedule.every().day.at("12:00").do(daily)
#nohup python model.py & in TERMINAL