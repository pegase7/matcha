from matcha.config import Config
# import logging
# from test2 import test2
from matcha.orm.data_access import DataAccess
# from matcha.model.Room import Room
# from matcha.model.Message import Message
# # from matcha.model.Users import Users
from matcha.web.util1 import hash_pwd
# import json
# import traceback
# import decimal

if __name__ == "__main__":
    data_access = DataAccess()
    userslist = data_access.fetch('Users', orderby='id')
    for users in userslist:
        print(users.id, hash_pwd('PasseMot0', users.user_name))
