from testunit.initTest import InitTestCase
from testunit.ormTest import OrmTestCase
from testunit.borisTest import BorisTestCase
from testunit.deleteBorisTest import DeleteBorisTestCase
from testunit.notificationCacheTest import NotificationCacheTestCase
from testunit.findProfileTest import FindProfileTestCase
from testunit.jsonTest import JsonTestCase
import unittest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(InitTestCase())
    suite.addTest(BorisTestCase())
    suite.addTest(DeleteBorisTestCase())
    suite.addTest(OrmTestCase())
    suite.addTest(NotificationCacheTestCase())
    suite.addTest(FindProfileTestCase())
    suite.addTest(JsonTestCase())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
