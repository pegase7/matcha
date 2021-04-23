import unittest
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from matcha.orm.data_access import DataAccess
import logging

class OrmTestCase(unittest.TestCase):

    def runTest(self):
        self.dataAccess = DataAccess()
        logging.info('Test init database')
        # connection = self.dataAccess.fetch('Connection', 1)
        # print(connection)
        # users = self.dataAccess.fetch('Users', 1)
        users1 = Users()
        users1.id = 1
        users2 = Users()
        users2.id = 1
        connection1 = Connection()
        try:
            connection1.id = 'a'
        except (TypeError):
            logging.info("Raise exception on connection1.id = 'a'") 
        connection2 = Connection()
        connection2.id = 1
        users = self.dataAccess.find('Users', 1)
        users.email = 'toto'
        print(users)

if __name__ == '__main__':
    unittest.main()
