import unittest
from matcha.model.Notification import Notification
from matcha.orm.data_access import DataAccess
from matcha.web.notification_cache import NotificationCache
import logging

class NotificationCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.addCleanup(self.cleanup)

    def runTest(self):
        print("\n")
        logging.info('   +-------------------------+')
        logging.info('   | Test Notification cache |')
        logging.info('   +-------------------------+')
        self.data_access = DataAccess()
        notification_cache = NotificationCache()
        notification_cache.init()
        self.assertEqual(3, len(notification_cache.cache), 'cache must contain 3 entry key!')
        self.assertEqual(7, notification_cache.get_unread(4), 'cache must contain 7 unread notifications for entry key 4!')
        newnotification = Notification()
        newnotification.sender_id = 1
        newnotification.receiver_id = 4
        newnotification.notif_type = 'Visit'
        newnotification.is_read = False
        notification_cache.persist(newnotification)
        self.assertEqual(8, notification_cache.get_unread(4), 'cache must contain 8 unread notifications for entry key 4 after persist!')
        self.newid = newnotification.id
        notif10 = self.data_access.find('Notification', 10)
        self.assertEqual(False, notif10.is_read, 'All notifications in cache must have unread status!')
        notif10.is_read = True
        notification_cache.merge(notif10)
        self.assertEqual(7, notification_cache.get_unread(4), 'cache must contain 7 unread notifications for entry key 4! after merge')

    def cleanup(self):
        notif10 = self.data_access.find('Notification', 10)
        self.assertEqual(True, notif10.is_read, 'Notification 10 must have read status!')
        notif10.is_read = False
        self.data_access.merge(notif10)
        newnotif = self.data_access.find('Notification', self.newid)
        self.data_access.remove(newnotif)
        

if __name__ == '__main__':
    unittest.main()
