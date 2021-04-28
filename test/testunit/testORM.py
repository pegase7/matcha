import unittest
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from matcha.orm.data_access import DataAccess
import logging

class OrmTestCase(unittest.TestCase):

    def runTest(self):
        self.data_access = DataAccess()
        users1 = Users()
        users1.id = 1
        users2 = Users()
        users2.id = 1
        connection1 = Connection()
        try:
            connection1.id = 'a'
            self.fail("Int control does not work on 'id' InField of 'Connection' model")
        except (TypeError):
            logging.info("Raise exception on connection1.id = 'a'") 
        connection2 = Connection()
        connection2.id = 1
        users = self.data_access.find('Users', 1)
        try:
            users.email = 'toto'
            self.fail("Email control does not work on 'email' EmailField of 'Users' model")
        except (TypeError):
            logging.info("Raise exception users.email = 'toto'") 
        print(users)

if __name__ == '__main__':
    unittest.main()
