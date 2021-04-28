from matcha.config import Config
from dataclasses import dataclass
# import logging
# from test2 import test2
from matcha.orm.data_access import DataAccess
# from matcha.model.Room import Room
# from matcha.model.Message import Message
# # from matcha.model.Users import Users
from matcha.model.Topic import Topic
from matcha.web.util1 import hash_pwd
# import json
# import traceback
# import decimal

if __name__ == "__main__":
    data_access1 = DataAccess()
    data_access2 = DataAccess()
    data_access = data_access1
    postgresqlconfig = Config().config['postgresql']
    
    topic1 = Topic()
    topic1.tag = 'tata'
    topic2 = Topic()
    topic2.tag = 'toto'
    print(topic1, topic2)
    # print('Ceci est un essai')
    # logging.debug(postgresqlconfig)
    # logging.info(postgresqlconfig)
    # logging.warning(postgresqlconfig)
    
    # i = decimal.Decimal(10).__int__()
    # print('i:', i, type(i))
    users = data_access.fetch('Users', orderby='id')
    data_access2 = DataAccess()
    for user in users:
        user.password = hash_pwd('PasseMot0', user.user_name)
        print(user.id, user.user_name, user.password)

    #     dataAccess.merge(user, autocommit=False)
    # dataAccess.commit()

