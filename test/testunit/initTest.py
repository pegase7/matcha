import unittest
import logging
from matcha.config import Config
from matcha.orm.data_access import DataAccess

class InitTestCase(unittest.TestCase):

    def runTest(self):
        data_access = None
        config = None
        try:
            config = Config(configpath='resources/configuration/configTest.json')
            ''' logging must be used after config initialization '''
            logging.info('   +-----------------------------+')
            logging.info('   | Test init config & database |')
            logging.info('   +-----------------------------+')
            data_access = DataAccess()
        except:
            self._outcome.result.shouldStop = True # Stop suite test
            self.assertIsNotNone(config, "configuration failed")
            self.assertIsNotNone(data_access, "Database connection failed")

if __name__ == '__main__':
    unittest.main()