#Graphs for Sleep, Diet and Activity

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import csv
from datetime import datetime


sleepdf = pd.read_csv('csv/sleep.csv', sep=';')
activitydf = pd.read_csv('csv/activity.csv')

#Seperate Start column to the Day slept, the start time and end time
sleepdf['Day'] = pd.to_datetime(sleepdf['Start']).dt.date  
sleepdf['Start'] = pd.to_datetime(sleepdf['Start']).dt.time
sleepdf['End'] = pd.to_datetime(sleepdf['End']).dt.time
sleepdf.rename(columns={'Sleep quality': 'SleepQuality','Time in bed': 'TimeInBed','Wake up': 'WakeUp','Sleep Notes': 'SleepNotes', 'Heart rate':'HeartRate', 'Activity (steps)':'Steps'}, inplace=True)

#creating Sleep Quality and Time graph
x = []
y = []

headers = ['Sleep Quality','Time']
print(sleepdf)

x = sleepdf['Day']
y = sleepdf['SleepQuality']

# plot
plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()

# def bar_chart(numbers, labels, pos):
#     plt.bar(pos, numbers, color='blue')
#     plt.xticks(ticks=pos, labels=labels)
#     plt.show()
# if __name__ == '__main__':
#     numbers = [2, 1, 4, 6]
#     labels = ['Electric', 'Solar', 'Diesel', 'Unleaded']
#     pos = list(range(4))
#     bar_chart(numbers, labels, pos)