import matcha.config
import logging
from test2 import test2
from matcha.orm.data_access import DataAccess
from matcha.model.Room import Room
from matcha.model.Message import Message
from matcha.model.Users import Users
import json
import traceback

if __name__ == "__main__":
    dataAccess = DataAccess()
    populateconfig = matcha.config.config['populate']
    
    print('Ceci est un essai')
    logging.debug(populateconfig)
    logging.info(populateconfig)
    logging.warning(populateconfig)

    users = dataAccess.find('Users', 1)
    print(users)
    