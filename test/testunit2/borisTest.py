import unittest
from matcha.model.Users import Users
from matcha.orm.data_access import DataAccess
import logging

class BorisTestCase(unittest.TestCase):

    def test_boris(self):
        dataAccess = DataAccess()
        logging.info('Test Boris')
        borises = dataAccess.fetch('Users', conditions=('user_name', 'borisjohnson'), joins=(['topics', 'asvisiteds', 'asvisitors', 'messages', 'connections', 'rooms']))
        if 0 < len(borises):
            for boris in borises:
                dataAccess.execute('delete from Users_topic where users_id = %s', parameters=[boris.id])
                dataAccess.execute('delete from Users_room where master_id = %s', parameters=[boris.id])
                dataAccess.execute('delete from Users_room where slave_id = %s', parameters=[boris.id])
                for visited in boris.asvisiteds:
                    dataAccess.remove(visited)
                for visitor in boris.asvisitors:
                    dataAccess.remove(visitor)
                for message in boris.messages:
                    dataAccess.remove(message)
                for connection in boris.connections:
                    dataAccess.remove(connection)
                for room in boris.rooms:
                    dataAccess.remove(room)
                dataAccess.remove(boris)
            
        borises = dataAccess.fetch('Users', conditions=('user_name', 'borisjohnson'))
        if 0 < len(borises):
            pass
        '''
        Create Users 'Boris'. All necessary fields must be initialized to avoid an error
        '''
        boris = Users()
        boris.first_name = 'Boris'
        boris.last_name = 'Johnson'
        boris.user_name = 'borisjohnson'
        boris.password = 'ElisabethGetOnMyNerves'
        boris.description = 'Blond, intelligent mais menteur'
        boris.email = 'boris.johnson@england.uk'
        boris.active = True
        boris.confirm = None
        boris.gender = 'Male'
        boris.orientation = 'Hetero'
        boris.birthday = '1964-06-19'
        boris.latitude = None
        boris.longitude = None
        boris.popularity = 10
        dataAccess.persist(boris)

if __name__ == '__main__':
    unittest.main()
