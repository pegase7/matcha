from matcha.config import Config
from matcha.model.Notification import Notification
from matcha.web.notification_cache import NotificationCache
import random
import logging
from faker import Faker

# from test2 import test2
from matcha.orm.data_access import DataAccess
# from matcha.model.Room import Room
# from matcha.model.Message import Message
# from matcha.model.Users import Users
# from matcha.web.util3 import compute_recommendations
# import json
# import traceback
# import decimal
# import base64

if __name__ == "__main__":
    data_access = DataAccess()
    # notification_cache = NotificationCache()
    # notification_cache.init()

    data_access.fetch('Users', 1)
    # for usersid in notification_cache.cache.keys():
    #     users = data_access.find('Users', usersid)
    #     print(users.first_name, users.last_name, users.user_name)
    #     print(notification_cache.get_unread(users.id))
    
    for i in range(5):
        print('i: ', i)

    fake = Faker(['fr_FR', 'fr_CA', 'fr_QC'])
    fake = Faker(['fr_CA'])
    
    for i in range(1,10):
        print('range' + str(i), fake.sentence())
        
    users10list = data_access.fetch('Users', conditions=('id', '<=','10'))
    print('id\tuser_name\t\tName')
    for users in users10list:
        print(users.id, '\t', users.user_name, '\t', users.first_name + ' ' + users.last_name)
