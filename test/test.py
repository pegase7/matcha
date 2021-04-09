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
    room = Room()
    room.users_ids = [1,2]
    room.active =True
    dataAccess.persist(room)
    
    print('Ceci est un essai')
    logging.debug(populateconfig)
    logging.info(populateconfig)
    logging.warning(populateconfig)
    list = dataAccess.fetch('Users_room',joins=[('master_id', 'US')])
    print(len(list))
    print('Ceci est un essai')
    test2()
    
    message = Message()
    message.id = 1
    message.room_id = 2
    message.sender_id = 3
#    message.chat = "Ceci est un texte"
#    message.created = date.today()
    users1 = dataAccess.find('Users', conditions=1)
    users2 = Users()
    print(users2)
    print('id', id)
    try:
        toto = json.dumps(users1, cls=matcha.config.FlaskEncoder)
        print('toto 1:', toto)
        toto = json.dumps([users1,users2], cls=matcha.config.FlaskEncoder)
        print('toto 2:', toto)
        logging.info('OK')
    except (Exception) as e:
        logging.info('KO:' + str(e))
        traceback.print_exc()
    