from matcha.orm.data_access import DataAccess

'''
Provides a way to work on a cache rather than on database when searching unread notifications for a users.
Otherwise, database would be queried every 5 seconds.
    - merge and persist on Notification must use NotificationCache functions instead of DataAccess functions.
    - get_unread gives numbers of unread notificationsß split in Like, Message, Visit, Dislike types for an User Id.
'''
class NotificationCache():
    
    def init(self):
        self.data_access = DataAccess()
        # cache: Dict Users id, set of unread notification ids.
        self.cache = {}
        # cache_index: Dict Notification,id, Notifications.
        self.cache_index = {}
        notifications = self.data_access.fetch('Notification', ('is_read', False))
        
        for notification in notifications:
            if not notification.receiver_id in self.cache:
                self.cache[notification.receiver_id] = set()
            self.cache[notification.receiver_id].add(notification.id)
            self.cache_index[notification.id] = notification

    def merge(self, notification, autocommit=True):
        if notification.is_read:
            try:
                notif_set = self.cache[notification.receiver_id]
                notif_set.discard(notification.id)
                del self.cache_index[notification.id]
            except KeyError:
                pass
        self.data_access.merge(notification, autocommit)

    def persist(self, notification, autocommit=True):
        self.data_access.persist(notification, autocommit)
        if not notification.receiver_id in self.cache:
            self.cache[notification.receiver_id] = set()
        self.cache[notification.receiver_id].add(notification.id)
        self.cache_index[notification.id] = notification

    def get_unread(self, receiver_id):
        try:
            notificationids = self.cache[receiver_id]
            like = message = visit = dislike  = 0
            for notifid in notificationids:
                notification = self.cache_index[notifid]
                if 'Like' == notification.notif_type:
                    like += 1
                elif 'Message' == notification.notif_type:
                    message += 1
                elif 'Visit' == notification.notif_type:
                    visit += 1
                elif 'Dislike' == notification.notif_type:
                    dislike += 1
            return like, message, visit, dislike
        except KeyError:
            return 0, 0, 0, 0