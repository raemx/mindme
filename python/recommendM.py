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

# query = "SELECT * FROM recoms" 
# cursor = conn.cursor(dictionary=True)
# cursor.execute(query)
# recoms = DataFrame(cursor.fetchall()

# query = "SELECT * FROM matrix1" 
# cursor = conn.cursor(dictionary=True)
# cursor.execute(query)
# matrix = cursor.fetchall()
# matrix = matrix.pivot_table(index='user', columns='recom', values='rating')
# matrix = matrix.fillna(0)

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

for index, row in recommend.iterrows():
    if "M" in row['ID']: #GET RECOMMENDATION THAT FITS THE TYPE (SLEEP = W)
        x = row['recom']
        y = datetime.datetime.now()
        recom = row['NHS'] #GET WRTITTEN RECOMMENDATION
        sql = "INSERT INTO recommendations (id, rmdn, timestamp) VALUES (%s, %s, %s)"#post the recommendation into the DB
        # CSV file that has more data on that specific recommendation and links to resources that are then displayed on the Resources Tab.
        var = (currentuser, x, y)
        cursor.execute(sql, var)
        conn.commit()
        break