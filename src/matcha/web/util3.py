from pathlib import Path
import os
from matcha.web.util1 import distanceGPS
from matcha.config import Config
from matcha.orm.data_access import DataAccess
from dateutil.relativedelta import relativedelta
from matcha.model.Users_recommendation import Users_recommendation
from matcha.model.Recommendation_topic import Recommendation_topic

RATIO_KMS = [1, 10, 25, 50, 100, 200, 500] # Ratio distance return 1 if distance < 1KM, 2 if < 10Km, 3 if <2km, ... 
RECOMMENDATION = Config().config['recommendation']
THRESHOLD = RECOMMENDATION['threshold']
NB_RECOMMENDATIONS = RECOMMENDATION['nb_recommendations']
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
        ratio_km = 60 if (distance < RATIO_KMS[0]) else 50 if distance < RATIO_KMS[2] else 40 if distance < RATIO_KMS[3] else 30 if distance < RATIO_KMS[4] else 20 if distance < RATIO_KMS[5] else 10 if distance < RATIO_KMS[6] else 0
        return distance, ratio_km
    else:
        return None, 0

def users_match_age(usr1, usr2):
    if usr1.birthday and usr2.birthday:
        diff_age = abs((usr1.birthday - usr2.birthday).days)
        if 0 == diff_age:
            return 70
        elif  731 < diff_age: #2 years
            return 50
        elif 1825 < diff_age: # 5 years
            return 30
        elif 3650 < diff_age: # 10 years
            return 20
        elif 7300 < diff_age: # 20 years
            return 10
        else:
            return 1
    else:
        return 0
    
def users_match_topics(topics1, size, topics2):
    if not len(topics1) or not len(topics2):
        return [], 0
    match = 0
    matched_tags = []
    for tag1 in topics1:
        i = 0
        for tag2 in topics2:
            if tag1.tag == tag2.tag:
                matched_tags.append(tag2)
                match += 1
            i += 1
    minimum = min(i, size)
    maximum = max(i, size)
    return matched_tags, (1 - ((minimum - match) / minimum)) * 100  * (minimum / maximum)
    
def compute_recommendations(usr, global_topics=None, global_recommend_count=None):
    '''
    Retrieve needed recommendation
        global_topics is a dictionary of list of topics 
    ''' 
    conditions=[]
    conditions.append(('active', True))
    conditions.append(('id', '!=', usr.id))
    
    whereaddonstr = 'not exists (select null from USERS_RECOMMENDATION UR where UR.sender_id = %s and UR.receiver_id = U.id)'
    whereaddonstr += ' and not exists (select null from VISIT where visited_id = %s and visitor_id = U.id and COALESCE(isblocked,False) = true )'
    whereaddonstr += ' and not exists (select null from VISIT where visited_id = U.id and visitor_id = %s and COALESCE(isblocked,False) = true  and COALESCE(isfake,False) = true)'
    whereaddonprm = [usr.id, usr.id, usr.id]
    if 'Hetero' == usr.orientation:
        conditions.append(('gender', 'Male' if 'Female' == usr.gender else 'Female'))
        whereaddonstr += " and (orientation is null or orientation in ('Hetero', 'Bi'))"
    elif 'Homo' == usr.orientation:
        conditions.append(('gender', usr.gender))
        whereaddonstr += " and (orientation is null or orientation in ('Homo', 'Bi'))"
    else:
        whereaddonstr += " and (orientation is null or orientation = 'Bi' or (orientation = 'Homo' and gender = %s) or (orientation = 'Hetero' and gender != %s))"
        whereaddonprm.extend([usr.gender, usr.gender])
        
    
    if global_recommend_count:
        current_count = global_recommend_count[usr.id]
    else:
        DATA_ACCESS.execute('delete from users_recommendation where sender_id=%s and is_rejected=false', parameters=[usr.id], autocommit=False)
        current_count = 0
    
    max_count = NB_RECOMMENDATIONS - current_count
    if max_count > 0:
        weighting = 0
        recommendations = []
        
        ''' users2.topics is used when global_topics is None ''' 
        joins = [] if global_topics else 'topics'
        for users in DATA_ACCESS.fetch('Users', conditions=conditions, whereaddon=(whereaddonstr, whereaddonprm), joins=joins):
            if not users.latitude is None or not users.longitude is None:
                distance, ratio_km = users_distance(usr.latitude, usr.longitude, users.latitude, users.longitude)
            else:
                ratio_km = 0
                distance = None
            if global_topics:
                try:
                    topics1 = global_topics[usr.id]
                except KeyError:
                    topics1 = []
                try:
                    topics2 = global_topics[users.id]
                except KeyError:
                    topics2 = []
            else:
                topics1 = usr.topics
                topics2 = users.topics
            
            matched_tags, topics_ratio = users_match_topics(topics1, len(topics1), topics2)
            age_ratio = users_match_age(usr, users)
            weighting = ratio_km + age_ratio + topics_ratio
            if weighting >= THRESHOLD:
                delta = abs(relativedelta(usr.birthday, users.birthday).years)
                recommendations.append((weighting, delta, age_ratio, ratio_km, distance, topics_ratio, users.id, matched_tags))
        if 0 != len(recommendations):
            i = 0
            for recommendation in sorted(recommendations, reverse=True):
                if i == max_count:
                    break
                users_recommendation = Users_recommendation()
                users_recommendation.sender_id = usr.id
                users_recommendation.receiver_id = recommendation[6]
                users_recommendation.weighting = recommendation[0]
                users_recommendation.age_diff = recommendation[1]
                users_recommendation.age_ratio = recommendation[2]
                users_recommendation.distance = recommendation[4]
                users_recommendation.dist_ratio = recommendation[3]
                users_recommendation.topics_ratio = recommendation[5]
                users_recommendation.is_rejected = False
                DATA_ACCESS.persist(users_recommendation, autocommit=False)
                for tag in recommendation[7]:
                    recommendation_topic = Recommendation_topic()
                    recommendation_topic.recommend_id = users_recommendation.id
                    recommendation_topic.tag = tag
                    DATA_ACCESS.persist(recommendation_topic, autocommit=False)
                   
                i = i + 1  
        DATA_ACCESS.commit()   