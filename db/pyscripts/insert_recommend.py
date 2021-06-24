from matcha.orm.data_access import DataAccess
from matcha.web.util3 import compute_recommendations

def populate():
    DATA_ACCESS = DataAccess()
    users_topics = DATA_ACCESS.fetch('Users_topic', orderby='users_id')
    currentusersid = -1   
    global_topics = {}
    global_recommend_count = {}
    for (key, value) in  DATA_ACCESS.execute("select sender_id, count(*) from USERS_RECOMMENDATION where is_rejected=false group by sender_id"):
        global_recommend_count[key] = value
    for users_topic in users_topics:
        if users_topic.users_id != currentusersid:   
            topics = []
            currentusersid = users_topic.users_id
            global_topics[currentusersid] = topics
        topics.append(users_topic)
        
    for users in DATA_ACCESS.fetch('Users'):
        compute_recommendations(users, global_topics, delete_existing_recommendation=True)