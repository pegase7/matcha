from pathlib import Path
import operator
import os
from matcha.web.util1 import distanceGPS
from matcha.config import Config
from matcha.orm.data_access import DataAccess
from dateutil.relativedelta import relativedelta
from matcha.model.Users_recommendation import Users_recommendation

RATIO_KMS = [1, 10, 25, 50, 100, 200, 500] # Ratio distance return 1 if distance < 1KM, 2 if < 10Km, 3 if <2km, ... 
POPULATE = Config().config['populate']
THRESHOLD = POPULATE['threshold']
NB_RECOMMENDATIONS = POPULATE['nb_recommendations']
DATA_ACCESS = DataAccess()


def is_recommadable(user):
    if user.gender is None:
        return False
    if user.orientation is None:
        return False
    photoPath = Path(__file__).parent.joinpath('static/photo')
    for path in  photoPath.rglob(user.user_name + '*.jpg'):
        for i in range(1,5):
            if os.path.basename(path) == user.user_name + str(i) + '.jpg':
                return True
    return False

def users_distance(lat1, lon1, lat2, long2):
    if not lat2 is None or not long2 is None:
        distance = distanceGPS(lat1, lon1, lat2, long2)
        ratio_km = 6 if (distance < RATIO_KMS[0]) else 5 if distance < RATIO_KMS[2] else 4 if distance < RATIO_KMS[3] else 3 if distance < RATIO_KMS[4] else 2 if distance < RATIO_KMS[5] else 1 if distance < RATIO_KMS[6] else 0
        return distance, ratio_km
    else:
        return None, 0

def users_match_age(usr1, usr2):
    if usr1.birthday and usr2.birthday:
        diff_age = abs((usr1.birthday - usr2.birthday).days)
        if 0 == diff_age:
            return 8
        elif  731 < diff_age: #2 years
            return 4
        elif 1825 < diff_age: # 5 years
            return 2
        elif 3650 < diff_age: # 10 years
            return 0
        elif 7300 < diff_age: # 20 years
            return -5
        else:
            return -8
    else:
        return 0
    
def users_match_topics(topics1, size, topics2):
    if not len(topics1) or not len(topics2):
        return 0
    match = 0
    for tag1 in topics1:
        i = 0
        for tag2 in topics2:
            match += (tag1 == tag2)
            i += 1
    minimum = min(i, size)
    maximum = max(i, size)
    return (1 - ((minimum - match) / minimum)) * 10  * (minimum / maximum)
    
def compute_recommendations(usr, global_topics=None, global_recommend_count=None):
    '''
    Retrieve needed recommendation
        global_topics is a dictionary of list of topics 
    ''' 
    conditions=[]
    conditions.append(('active', True))
    if 'Hetero' == usr.orientation:
        conditions.append(('gender', 'Male' if 'Female' == usr.gender else 'Male'))
    elif 'Homo' == usr.orientation:
        conditions.append(('gender', usr.gender))
    
    if global_recommend_count:
        current_count = global_recommend_count[usr.id]
    else:
        current_count = DATA_ACCESS.execute('select count(*) from USERS_RECOMMENDATION where sender_id = %s and is_rejected=false', [usr.id], autocommit=False)[0][0]
    max_count = NB_RECOMMENDATIONS - current_count
    if max_count > 0:
        weighting = 0
        recommendations = []
        
        ''' users2.topics is used when global_topics is None ''' 
        joins = [] if global_topics else 'topics'
        for users in DATA_ACCESS.fetch('Users', conditions=conditions, whereaddon='not exists (select null from USERS_RECOMMENDATION UR where UR.sender_id = U.id)', joins=joins):
            if usr.id != users.id:
                if not users.latitude is None or not users.longitude is None:
                    distance, ratio_km = users_distance(usr.latitude, usr.longitude, users.latitude, users.longitude)
                else:
                    ratio_km = 0
                    distance = None
                topics1 = global_topics[usr.id] if global_topics else usr.topics
                topics2 = global_topics[users.id] if global_topics else users.topics
                
                topics_ratio = users_match_topics(topics1, len(topics1), topics2)
                weighting = ratio_km + users_match_age(usr, users) + topics_ratio
                if weighting >= THRESHOLD:
                    delta = abs(relativedelta(usr.birthday, users.birthday).years)
                    recommendations.append((weighting, delta, ratio_km, distance, topics_ratio, users.id))
        if 0 != len(recommendations):
            i = 0
            for recommendation in sorted(recommendations, reverse=True):
                if i == max_count:
                    break
                users_recommendation = Users_recommendation()
                users_recommendation.sender_id = usr.id
                users_recommendation.receiver_id = recommendation[5]
                users_recommendation.weighting = recommendation[0]
                users_recommendation.age_diff = recommendation[1]
                users_recommendation.distance = recommendation[3]
                users_recommendation.dist_ratio = recommendation[2]
                users_recommendation.topics_ratio = recommendation[4]
                users_recommendation.is_rejected = False
                DATA_ACCESS.persist(users_recommendation, autocommit=False)
                i = i + 1  
        DATA_ACCESS.commit()   

