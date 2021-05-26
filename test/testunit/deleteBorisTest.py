import unittest
from matcha.orm.data_access import DataAccess
import logging

class DeleteBorisTestCase(unittest.TestCase):

    def runTest(self):
        print("\n")
        logging.info('   +-------------------+')
        logging.info('   | Test delete Boris |')
        logging.info('   +-------------------+')
        data_access = DataAccess()
        borises = data_access.fetch('Users', conditions=('user_name', 'borisjohnson'), joins=(['asvisiteds', 'asvisitors', 'messages', 'connections', 'rooms']))
        self.assertEqual(len(borises), 1, "User Boris (username='borisjohnson') does not exist!")
        boris = borises[0]
        ''' delete Users_topics by sql because users.topic returns topic (see Users_topic.py file''' 
        data_access.execute('delete from Users_topic where users_id = %s', parameters=[boris.id])
        for room in boris.rooms:
            for users_room in data_access.fetch('Users_room', conditions=[('room_id', room.id)]):
                data_access.remove(users_room, autocommit=False)
        for visited in boris.asvisiteds:
            data_access.remove(visited, autocommit=False)
        for visitor in boris.asvisitors:
            data_access.remove(visitor, autocommit=False)
        for message in boris.messages:
            data_access.remove(message, autocommit=False)
        for connection in boris.connections:
            data_access.remove(connection, autocommit=False)
        for room in boris.rooms:
            data_access.remove(room, autocommit=False)
        data_access.remove(boris)

        ''' Delete mock topic '''
        for tag in ['#java#', '#sieste#']:
            topic = data_access.find('Topic', tag)
            self.assertIsNotNone(topic, "Topic '" + tag +"' does not exist!")
            data_access.remove(topic, autocommit=False)
        data_access.commit()
        logging.info('Test delete Boris is ok')
        

if __name__ == '__main__':
    unittest.main()
