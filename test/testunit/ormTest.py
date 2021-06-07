import unittest
import logging
from matcha.orm.data_access import DataAccess
from matcha.config import Config

class OrmTestCase(unittest.TestCase):

    def runTest(self):
        print("\n")
        logging.info('   +----------+')
        logging.info('   | Test ORM |')
        logging.info('   +----------+')
        data_access = DataAccess()
        users1 = data_access.find('Users', 1)
        users1.popularity = 'a'
        try:
            data_access.merge(users1, autocommit=False)
            self.fail("Int control does not work on 'popularity' InField of 'Users' model")
        except (TypeError):
            logging.info("Raise exception (popularity must be int value) on users1.popularity = 'a'") 
        try:
            users1.email = 'toto'
            data_access.merge(users1, autocommit=False)
            self.fail("Email control does not work on 'email' EmailField of 'Users' model")
        except (TypeError):
            logging.info("Raise exception (invalid email) users.email = 'toto'") 
        room1 = data_access.find('Room', 1)
        self.assertIsNotNone(room1.users_ids, 'Room.users_ids must not be null')
        userslist = data_access.fetch('Users', orderby='id', limit=3)
        self.assertEqual(3, len(userslist), 'limit must be 3!')
        
        userslist = data_access.fetch('Users', whereaddon=(('id between %s and %s',[5,16])))
        self.assertEqual(12, len(userslist), 'Whereaddon test returns wrong count of rows!')

if __name__ == '__main__':
    Config(configpath='resources/configuration/configTest.json')
    unittest.main()
