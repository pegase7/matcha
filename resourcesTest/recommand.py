from matcha.model.Users import Users
from matcha.model.Users import Users
from matcha.orm.data_access import DataAccess
from matcha.web.util3 import compute_recommendations
from datetime import datetime

DATA_ACCESS = DataAccess()
TOPICS = {}

if __name__ == "__main__":
    starttime = datetime.now()
    for usr in DATA_ACCESS.fetch('Users'):
        TOPICS[usr.id] = DATA_ACCESS.fetch('Users_topic', ('users_id', usr.id))
    for usr in DATA_ACCESS.fetch('Users', conditions=[('active', True),('id','<',10000)], joins='topics'):
        compute_recommendations(usr, TOPICS)
    endtime = datetime.now()
    print('END', str(endtime - starttime))