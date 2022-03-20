#Models for Recommendations - Seperate for Mood vs other factors
import math 
import random
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import tensorflow
import gym
import keras
from datetime import date
from gym import Env
from gym.spaces import Discrete, Box #define actions and state in env
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from rl.agents import DQNAgent #agents used to train reinforcement model
from rl.policy import BoltzmannQPolicy #policy based reinforcment model
from rl.memory import SequentialMemory #maintaining memory for model

sleepdf = pd.read_csv('sleep.csv')
activitydf = pd.read_csv('activity.csv')

#Seperate Start column to the Day slept, the start time and end time
#sleepdf[['DaySlept','BeginTime']] = sleepdf['Start'].str.split(' ', 1, expand=True) #BeginTime for start time of sleeping
sleepdf['Day'] = pd.to_datetime(sleepdf['End']).dt.time #DAY WAKEN UP FROM SLEEP
sleepdf.rename(columns={'Sleep quality': 'SleepQuality','Time in bed': 'TimeInBed','Wake up': 'WakeUp','Sleep Notes': 'SleepNotes', 'Heart rate':'HeartRate', 'Activity (steps)':'Steps'}, inplace=True)
# VARIABLES FOR GRAPH: BEGINTIME(TIME), DAY(WOKEN UP), SLEEPQUALITY, TIMEINBED

activitydf['Steps'] = activitydf['Steps'].replace(",", "", regex=True)
activitydf['Steps'] = activitydf['Steps'].notna.astype(int)




testdf = pd.DataFrame.from_dict({
    'Day': ['15-Apr', '16-Apr', '17-Apr', '18-Apr'], 
    'Steps': [9693, 6000, 11596, 2000]
    })

# RANDOM QUESTIONS TO USERS
#
#
#
#
#
#

q = ["HOW ARE YOU TODAY?","HOW IS THE DAY GOING FOR YOU?", "LET ME KNOW HOW YOU'RE FEELING", "HOW IS THE DAY TREATING YOU?","ARE YOU DOING WELL TODAY?"]
day = 0

if testdf.iloc[day, 0] == datetime.today().date():
    # checkifdatahasbeenadded(); - a trigger in dataset to check if theres more data added because it's the next day
    day += 1
    print(q[random.randrange(5)])
else:
    print(q[random.randrange(5)])

#Recommendation Model
#
#
#
#
#
#
#
class MindEnv(Env):
    def __init__(self):
        # Actions: Steps >= 8000, Steps between 5 and 8 000, Steps under 5000
        self.action_space = Discrete(3) #0 , 1, 2 ??????
        # Steps array - current steps for day
        self.observation_space = Box(low=np.array([0]), high=np.array([40000]))
        # Set start steps
        self.state = 0
        # Set time frame the steps are measured for - a single day
        self.time = 86400
        self.day = 0
        self.timecount = 0 

        #after every 7 days, weekly (7,14,21, 28->0, repeat), every month(30,60,90), every 3 months() 
        #if hit on same day, do largest one
        #recommend - every day, general recommend,
        
    def step(self, action):
        # Apply action
        # 0 +steps 
        # 1 +steps
        # 2 +steps
        # 
        # while self.day <= len(testdf):
        self.state += action + testdf.iloc[day, 1]
        #Moves to next day y
        self.time -= 86400
        self.day += 1
    
        # Calculate reward
        if self.state >= 8000: 
            reward = 3 
        elif 5000 <= self.state < 8000:
            reward = 2
        else:
            reward = 1 

        #calculate for time period
        #if self.i == 7:

    
    # # Check if day is done
        if self.time <= 0: 
             done = True
        else:
             done = False
            
        # Apply temperature noise
        #self.state += random.randint(-1,1)
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        # Reset steps for a new day 
        self.state = 0
        # Reset day
        self.time = 86400
        return self.state
    
env = MindEnv() #create environment
# example = env.action_space.sample()
# print(example)
states = env.observation_space.shape[0]
actions = env.action_space.n

episodes = 7 #7 days of steps measuring - 
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        env.render()
        action = random.choice([0,1,2]) 
        action = env.action_space.sample() #0, 1 or 2
        n_state, reward, done, info = env.step(action) #apply action to environment
        score+=reward #calculate reward
    print('Episode:{} Score:{}'.format(episode, score))




def build_model(states, actions): 
    model = Sequential() 
    model.add(Flatten(input_shape=(1,states))) #passing flatten node, flat node with all the different states
    model.add(Dense(24, activation='relu')) #2 dense nodes with relu activation function - fully connected layers in neurwal network
    model.add(Dense(24, activation='relu')) # pass through actions down bottom  - pass them out for environments
    model.add(Dense(actions, activation='linear'))
    return model

model = build_model(states, actions)
model.summary()

#take build_model (model) and train it with KerasRL

def build_agent(model, actions): 
    policy = BoltzmannQPolicy() #identify policy
    memory = SequentialMemory(limit=50000, window_length=1) #set up memory
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
                  nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2) #pass deep leanring model, memory and policy
    return dqn

dqn = build_agent(model, actions) #used this to build dqn model
dqn.compile(Adam(lr=1e-3), metrics=['mae']) # pass optimizer and metrics to track
dqn.fit(env, nb_steps=50000, visualize=False, verbose=1) # pass nenvrionment, steps, visualisation and little logging

# scores = dqn.test(env, nb_episodes=100, visualize=False)
# print(np.mean(scores.history['episode_reward']))
# _ = dqn.test(env, nb_episodes=15, visualize=True)

# dqn.save_weights('dqn_weights.h5f', overwrite=True)
# del model
# del dqn
# del env

# env = gym.make('CartPole-v0')
# actions = env.action_space.n
# states = env.observation_space.shape[0]
# model = build_model(states, actions)
# dqn = build_agent(model, actions)
# dqn.compile(Adam(lr=1e-3), metrics=['mae'])
# dqn.load_weights('dqn_weights.h5f')
# _ = dqn.test(env, nb_episodes=5, visualize=True)




# RANDOM RECOMMENDATIONS NOTIFICATIONS