import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator
import mysql.connector
import datetime

#establishing the connection
conn = mysql.connector.connect(
   user='root', host='localhost', database='mindme')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#usee php to identify what CURRENT user IS


"""Collaboration Filtering - User to User  """
"""Using user raings of each recommendartion (based on their performance) to recommend recommendations to other users of similar habits"""

matrix = pd.read_csv("../csv/matrix1.csv", index_col=0 ) #The NAN data given 0 - where users havent seen the matrixmendation yet
recoms = pd.read_csv("../csv/recoms.csv")
matrix = matrix.pivot_table(index='user', columns='recom', values='rating')
matrix = matrix.fillna(0)

currentuser = 1
recom = 'random recommendation'

def simuser(user, m, k=3):
    other = m[m.index != user] #dataframe of users who aren;t the user to be recommeded
    user = m[m.index == user] #dataframe of user to find similar users for
    sim = cosine_similarity(user,other)[0].tolist() #using cosine similarity to find how similar the two are
    indices = other.index.tolist() #list of users indexes who are similar
    indexsim = dict(zip(indices, sim)) #k/v pairs of user's index and similarity
    indexsim_sorted = sorted(indexsim.items(), key=operator.itemgetter(1)) #sort top down by similarity
    indexsim_sorted.reverse() 

    top_users_similarities = indexsim_sorted[:k] #get top "k" users
    users = [u[0] for u in top_users_similarities] 
    
    return users
    

simuserindex = simuser(currentuser, matrix)

def recommend_item(user_index, simuserindex, m, items=5):
    
    #load vectors for similar users and get avg rating 
    simuser = m[m.index.isin(simuserindex)]
    simuser = simuser.mean(axis=0)
    simuser_df = pd.DataFrame(simuser, columns=['mean'])
    
    
    # load vector for the current user, transpose, rename column, remove rows with 0
    user_df = m[m.index == user_index]
    user_df_transposed = user_df.transpose()
    user_df_transposed.columns = ['rating']
    user_df_transposed = user_df_transposed[user_df_transposed['rating']==0]
    recoms_unseen = user_df_transposed.index.tolist()
    
    # filter avg ratings of similar users for only recom the current user has not seenm order, get top n and lookup in other csv for info
    simuser_df_filtered = simuser_df[simuser_df.index.isin(recoms_unseen)]
    simuser_df_ordered = simuser_df.sort_values(by=['mean'], ascending=False)
    top_n_recom = simuser_df_ordered.head(items)
    top_n_recom_indices = top_n_recom.index.tolist()
    recom_information = recoms[recoms['recom'].isin(top_n_recom_indices)]
    
    return recom_information #items
# try it out
recommend = recommend_item(currentuser, simuserindex, matrix)
print(recommend)
for index, row in recommend.iterrows():
    if "W" in row['ID']: #GET RECOMMENDATION THAT FITS THE TYPE (SLEEP = W)
        x = row['recom']
        y = datetime.datetime.now()
        recom = row['NHS'] #GET WRTITTEN RECOMMENDATION
        print(row['recom'])
        sql = "INSERT INTO recommendations (id, rmdn, timestamp) VALUES (%s, %s, %s)"#post the recommendation into the DB
        # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
        var = (currentuser, x, y)
        cursor.execute(sql, var)
        conn.commit()
        break

# """Matrix Refactorization """

# """Brings mean that user gives to 0"""

# """Corrects data for users that can be too harsh"""
# def standardize(row):
#     new_row = (row - row.mean()) / (row.max()-row.min()) #range of rating user gives
#     return row

# matrix_std = matrix.apply(standardize)

# user_sim = cosine_similarity(matrix_std)#similarity matrix column wise needed therefore transpose 
# user_sim_df = pd.DataFrame(user_sim, index=matrix.index, columns=matrix.index) #create df from user similarity making users as both column and row header to see how related users are to each other 

# def getUser(user, val): #returns similarity score for all matrixmendations that combine well with this matrix
#     sim_score = user_sim_df[user]*(val-2.5)  #get user similarity for that given matrix, scale it with how their average changed based on the matrix
#     #subtracted by mean(2.5) due to the fact that if a user his unsimilar to another, we do not want other similar unsuitable user to appear at the top of list
#     sim_score = sim_score.sort_values(ascending=False) #descending order
#     return sim_score

# sim_user = pd.DataFrame()

#  = [('SR1', 5), ('SR2', 1), ('SR3', 3)] #example data of a user who recieves sleep notifications often
# sim_user = pd.DataFrame()

# for user, val in non_sleeper:
#     sim_user = sim_user.append(getUser(user, val), ignore_index=True) #allows for multiple data insertion

# print(sim_user.sum().sort_values(ascending=False)) ##show all similar users


#mostsim = sim_user.idmax() ##find most similar user's id

#activitydf.loc[mostsim, 'day'] ##locate matrixmendation user requires by highest rating matrix by this similar user

# for index, row in df.iterrows():
#     if row == user:

#     if row == mostsim:
#         matrix.max(axis=1).['SR1']

