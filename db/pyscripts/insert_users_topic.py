from matcha.orm.data_access import DataAccess
from matcha.model.Users_topic import Users_topic
import numpy as np

def insert_topics(dataAccess, users_id, keys, values):
    nbtopics = np.random.randint(2,9)
    topics = np.random.choice(keys, nbtopics, replace=False, p=values)
    for topic in topics:
        usersTopic = Users_topic()
        usersTopic.users_id = users_id
        usersTopic.tag = topic
        dataAccess.persist(usersTopic, autocommit=False)
    
def populate(men_topic_dict, women_topic_dict):
    dataAccess = DataAccess()
    userslist = dataAccess.fetch('Users')
    womenkeys = np.array(list(women_topic_dict.keys()))
    womenvalues = np.array(list(women_topic_dict.values()))
    menkeys = np.array(list(men_topic_dict.keys()))
    menvalues = np.array(list(men_topic_dict.values()))
    womentotal = 0
    mentotal = 0
    for p in womenvalues:
        womentotal += p
    for p in menvalues:
        mentotal += p
    for users in userslist:
        if users.gender == 'Female':
            insert_topics(dataAccess, users.id, womenkeys, womenvalues)
        else:
            insert_topics(dataAccess, users.id, menkeys, menvalues)
    dataAccess.commit()