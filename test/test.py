from matcha.config import Config
# import logging
# from test2 import test2
from matcha.orm.data_access import DataAccess
# from matcha.model.Room import Room
# from matcha.model.Message import Message
# # from matcha.model.Users import Users
from matcha.web.util3 import compute_recommendations
# import json
# import traceback
# import decimal

if __name__ == "__main__":
    data_access = DataAccess()
    result = data_access.fetch('Users',1, joins='topics')
    print(result)
    print(compute_recommendations(result[0]))
