from matcha.model.Users import Users
from math import sin, cos, sqrt, atan2, radians
from matcha.model.Users import Users
from matcha.orm.data_access import DataAccess

EARTH_RADIUS = 6373.0
RATIO_KMS = [1, 10, 25, 50, 100, 200, 500] # Ratio distance return 1 if distance < 1KM, 2 if < 10Km, 3 if <2km, ... 

def users_distance(lat1, lon1, usr2):
    if not usr2.latitude is None or not usr2.longitude is None:
        lat2 = radians(usr2.latitude)
        lon2 = radians(usr2.longitude)
    
        a = sin(lat2 - lat1 / 2)**2 + cos(lat1) * cos(lat2) * sin(lon2 - lon1 / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
        distance = EARTH_RADIUS * c # distance in km
        ratio_km = 6 if (distance < RATIO_KMS[0]) else 5 if distance < RATIO_KMS[2] else 4 if distance < RATIO_KMS[3] else 3 if distance < RATIO_KMS[4] else 2 if distance < RATIO_KMS[5] else 1 if distance < RATIO_KMS[6] else 0
        return distance, ratio_km
    else:
        return -2, 0

def users_match_age(usr1, usr2):
    if usr1.birthday and usr2.birthday:
        o = usr1.birthday - usr2.birthday
        print(type(o))
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
    
def users_match_topics(tags, size, usr2):
    dataAccess = DataAccess()
    match = 0
    for tag1 in tags:
        i = 0
        for tag2 in dataAccess.fetch('USERS_TOPIC'):
            match += (tag1 == tag2)
            i += 1
    minimum = min(i, size)
    maximum = max(i, size)
    return (1 - ((minimum - match) / minimum)) * 10  * (minimum / maximum)
    
def compute_recommandations(usr):
    dataAccess = DataAccess()
    conditions=[]
    if 'Hetero' == usr.orientation:
        conditions.append(('gender', 'Male' if 'Female' == usr.gender else 'Male'))
    elif 'Homo' == usr.orientation:
        conditions.append(('gender', usr.gender))
    else: # bi
        conditions.append(('orientation', usr.orientation))
    
    recommand_count = 0
    max_count = dataAccess.execute('select count(*) from USERS_RECOMMANDATION where receiver_id = %s', [usr.id])
    threshold = 10
    ponderation = 0
    usr.tags()
    for users in dataAccess.fetch('Users', conditions=conditions, whereaddon='not exists (select null from USERS_RECOMMANDATION UR where UR.receiver_id = U.id)'):
        print(usr.id, users.id)
        if usr.id != users.id:
            if 8 == users.id:
                print(usr.id, users.id)
            if not users.latitude is None or not users.longitude is None:
                lat1 = radians(users.latitude)
                lon1 = radians(users.longitude)
                distance, ratio_km = users_distance(lat1, lon1, users)
            else:
                ratio_km = 0
                distance = 1
            ponderation = ratio_km + users_match_age(usr, users) + users_match_topics(usr, users)
            if ponderation >= threshold:
                print('Recommandation', ponderation, users)



if __name__ == "__main__":
    usr = DataAccess().find('Users',1)
    compute_recommandations(usr)