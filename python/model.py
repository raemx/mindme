"""Models for Recommendations - Seperate for Mood vs other factors"""
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
from sklearn import model_selection, metrics, linear_model
from IPython.display import display

# app = Flask(__name__)

# api = Api(app)
# CORS(app)

# @app.route("/home")
# def hello():
#     return jsonify({'text':'Hello World!'})

# if __name__ == '__main__':
#     app.run(port=8100)


"""Cleaning and Importing Data """
activitydf = pd.read_csv('../csv/activity.csv')
sleepdf = pd.read_csv('../csv/sleep.csv')
datadf = pd.read_csv('../csv/data.csv')
preddf = pd.read_csv('../csv/pred.csv')

sleepdf['day'] = pd.to_datetime(sleepdf['End']).dt.date #day finished sleeping
sleepdf['day'] = sleepdf['day'].to_string()
sleepdf['starttime'] = pd.to_datetime(sleepdf['Start']).dt.time #time began sleeping
sleepdf.rename(columns={'Sleep quality': 'sleepquality','Time in bed': 'timeinbed','Wake up': 'wakeup','Sleep Notes': 'sleepnotes', 'Heart rate':'heartrate', 'Activity (steps)':'steps'}, inplace=True)


activitydf.rename(columns={'Minutes Sedentary': 'minsed', 'Steps': 'steps', 'Day': 'day'}, inplace=True)
activitydf['steps'] = activitydf['steps'].replace(",", "", regex=True)
activitydf['steps'] = activitydf['steps'].astype(float)
activitydf['day'] = activitydf['day'].replace("-", "", regex=True)
activitydf['day'] = pd.to_datetime(activitydf['day'], format='%Y%m%d')

"""Creating Linear Models"""



#class Graphs():
"""DAY VS STEPS GRAPH"""

xticks = activitydf.day
day = [k for k in range(len(activitydf.day))] #must convert x axis to float therefore 1 is day 1 of recording
plt.scatter(day, activitydf.steps) 
plt.title('Your Steps This Week')
plt.xticks(day, xticks)
#plt.show() #scatter graph and ordered y axis.


"""PREDICTING DAY VS STEPS BASED ON PAST """
reg = linear_model.LinearRegression() #np.array(day).reshape(-1, 1)
reg.fit(np.array(day).reshape(-1, 1), activitydf.steps)#convert list to array, reshape from 1D array to 2D, train linear regrrssion model with available datapoints
#reg.predict([[30]]) #predicts value for 30th Day
stepscoef = reg.coef_ #coeeficient of graph
stepsinter = reg.intercept_ #interpcept

count3 = 0 #when reached 3 - 9 months
count1 = 0
count7 = 0
prevlen = 7
cols = ['predday', 'predstep']


"""PREDICTING DAY VS STEPS BASED ON PAST WEEK """

def dsgraph():
    predstep = []
    count=0 #place to insert data

    if len(activitydf)%84 == 0: #3 months 
        count3 += 1
        print("yes")
    elif len(activitydf)%28 == 0: #1 month
        count1 += 1
        print("y")
    elif len(activitydf)%7  == 0: #7 days #activitydf['day'].between(int(prevlen), activitydf.shape[1]
        ps = []
        for i in range(prevlen, len(activitydf)+7): #0-6 activity, 7-13 
            preddays = activitydf.loc[i-7, 'day'] + timedelta(days=7) #gets the next 7 days one by one
            predsteps = reg.predict(np.array([[i]])) #predicts steps for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
            predstep += predsteps # add pred steps for that day in DB
            ps.append([preddays, predsteps])
            #ps = pd.DataFrame([[preddays, predsteps]], columns =['predday', 'predstep']) # puts the next predicted day up to 7 days steps in df
            #ps.to_csv('../csv/pred.csv', index=count) #put day and step in DB
            #xticks += preddays #temporary
            count += 1
        preddf['predstep'] = preddf['predstep'].replace("[]", "", regex=True)
        preddf = pd.DataFrame(ps, columns=cols)
        xticks = preddf.predday
        preddaysnum = [k for k in range(len(preddf.predday))] #must convert x axis to float therefore 1 is day 1 of recording
        display(preddf)
        plt.scatter(preddaysnum, preddf.predstep) #creates graph of next week prediction
        plt.xticks(preddaysnum, xticks)
        plt.title('Next Weeks Predicted Steps')
        plt.show()
        avgpredstep = sum(predstep) / len([predstep]) #find average of the predicted step count 
        count7 += 1 #keep a count of how many 7 days passed
        prevlen = len(activitydf)+8 # keep track of last predicted 7 days

#dsgraph()
#def dmgraph():
    # plt.scatter(day, datadf.mood) 
    # plt.xticks(day, xticks)
    # currentmood = plt.show()

    # """DAY VS MOOD""" 
    # datadf['pred'] = 0 #create column with predictions of 0
    # if len(datadf)%84 == 0: #3 months 
    #     count3 += 1
    # elif len(datadf)%28 == 0: #1 month
    #     count1 += 1
    # elif len(datadf)%7  == 0: #7 days #activitydf['day'].between(int(prevlen), activitydf.shape[1]
    #     predmood = reg.predict(np.array([[int(prevlen), activitydf.shape[1]]]))#predicts steps for next 7 days: by looking which was last calc looks at 1 - 7, 8-14 etc
    #     nextdays = [d for d in range(prevlen+1, len(activitydf.length))]
    #     plt.scatter(np.array(nextdays).reshape(-1, 1), predmood) #creates graph of next week prediction
    #     plt.title('Next Weeks Predicted Mood')
    #     predM = plt.show()
    #     avgpredmood = sum(predmood) / len([predmood]) #find average of the predicted step count 
    #     activitydf.loc[df.index[len(datadf.shape[1])], 'pred'] = avgpredmood #last row of data: add avg step pred
    #     count7 += 1 #keep a count of how many 7 days passed
    #     prevlen = len(datadf.shape[1]) # keep track of last predicted 7 days
    #     print("ys")

"""SLEEP QUALITY VS BEGINTIME(TIME)"""
# plt.scatter(sleepdf.sleepquality, sleepdf.time) 
# plt.show()

"""DAY VS TIMEINBED"""
# plt.scatter(day, sleepdf.timeinbed) 
# plt.xticks(day, xticks)
# plt.show()



"""Test Data Frame"""

testdf = pd.DataFrame.from_dict({
    'Day': ['15-Apr', '16-Apr', '17-Apr', '18-Apr'], 
    'Steps': [9693, 6000, 11596, 2000]
    })

"""Creating Deep Learning Model for Predictions"""
class MindMe:
    def __init__(self, user, day, steps, minsed): # starttime, timeinbed, sleepquality, cal):
        self.user = user
        self.day = day
        self.steps = steps
        self.minsed = minsed
        # self.tib = timeinbed
        # self.start = starttime
        # self.qual = sleepquality
        # self.cal = cal
    

    def __len__(self):
        return len(self.user)

    def __getitem__(self, item):
        user = self.user[item]
        day = self.day[item]
        steps = self.steps[item]
        minsed = self.minsed[item]
        # tib = self.tib[item]
        # start = self.start[item]
        # qual = self.qual[item]
        # cal = self.cal[item]

        return {
            "user": torch.tensor(user, dtype=torch.int),
            "days": torch.tensor(day, dtype=torch.date),
            "steps": torch.tensor(steps, dtype=torch.int),
            "minsed": torch.tensor(minsed, dtype=torch.int)        
            # "tib": torch.tensor(tib, dtype=torch.time),
            # "start": torch.tensor(start, dtype=torch.time),
            # "qual": torch.tensor(qual, dtype=torch.int),
            # "cal": torch.tensor(cal, dtype=torch.int)
        }

class RecSysModel(tez.Model):
    def __init__(self, usercount, stepscount):
        super().__init__()
        self.user_embed = nn.Embedding(usercount, 32)
        self.steps_embeed = nn.Embedding(stepscount, 32)
        self.out = nn.Linear(64, 1)
        self.step_scheduler_after = "epoch"

    def fetch_optimizer(self):
        opt = torch.optim.Adam(self.parameters(), lr=1e-3)
        return opt

    def fetch_scheduler(self):
        sch = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=3, gamma = 0.7)
        return opt

        """METRICS TO MONITOR"""

    def monitor_metrics(self, output, steps):
        output = output.detach().cpu().numpy()
        steps = steps.detach().cpu().numpy()
        return {
            'rmse':  np.sqrt(metrics.mean_squared_error(steps, output))
        }
        
    def forward(self, user, day, steps):
        user_embeds = self.days.user_embed(days)
        steps_embeds = self.days.steps_embed(days)
        output = torch.cat([user_embeds, steps_embeds], dim=1)
        output = self.out(output)

        loss = nn.MSELoss()(output, steps.view(-1, 1))
        calc_metrics = self.monitor_metrics(output, ratings.view(-1,1))
        return output, loss, calc_metrics 

    def train():
        """Reading and Cleaning csv data

        Editing and adding columns 
        """
        sleepdf = pd.read_csv('../csv/sleep.csv')
        sleepdf['day'] = pd.to_datetime(sleepdf['End']).dt.date #day finished sleeping
        sleepdf['starttime'] = pd.to_datetime(sleepdf['Start']).dt.time #time began sleeping
        sleepdf.rename(columns={'Sleep quality': 'sleepquality','Time in bed': 'timeinbed','Wake up': 'wakeup','Sleep Notes': 'sleepnotes', 'Heart rate':'heartrate', 'Activity (steps)':'steps'}, inplace=True)
        
        activitydf = pd.read_csv('../csv/activity.csv')
        activitydf.rename(columns={'Minutes Sedentary': 'minsed', 'Steps': 'steps', 'Day': 'day'}, inplace=True)
       
        lbl_user = preprocessing.LabelEncoder()
        lbl_steps = preprocessing.LabelEncoder()

        activitydf.user = lbl_user.fit_transform(activitydf.user.values)
        activitydf.steps = lbl_steps.fit_transform(activitydf.steps.values)

        """Training the csv data - SPLIT DATA""" 
        activitydf_train, activitydf_valid = model_selection.train_test_split(
            activitydf, test_size=0.33, random_state=42
        )
        
        train_dataset = MindMe(
            user = activitydf_train.user.values, steps = activitydf_train.steps.values, day = activitydf_train.day.values
        )

        valid_dataset = MindMe(
            user = activitydf_valid.user.values, steps = activitydf_valid.steps.values, day = activitydf_valid.day.values 
        )

        model = RecSysModel(usercount=len(lbl.user.classes_), stepscount = len(lbl_steps.classes_))
        model.fit(
            train_dataset, valid_dataset, train_bs = 1024, valid_bs=1024, fp16=True
        )
       
#MindMe.train()

