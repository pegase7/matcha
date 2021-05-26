from matcha.orm.data_access import DataAccess

class NotificationCache():
    
    def init(self):
        self.data_access = DataAccess()
        self.cache = {}
        notifications = self.data_access.fetch('Notification', ('is_read', False))
        for notification in notifications:
            if not notification.receiver_id in self.cache:
                self.cache[notification.receiver_id] = set()
            self.cache[notification.receiver_id].add(notification.id)

    def merge(self, notification):
        if notification.is_read:
            try:
                notif_set = self.cache[notification.receiver_id]
                notif_set.discard(notification.id)
            except KeyError:
                pass
        self.data_access.merge(notification)

    def persist(self, notification):
        self.data_access.persist(notification)
        if not notification.receiver_id in self.cache:
            self.cache[notification.receiver_id] = set()
        self.cache[notification.receiver_id].add(notification.id)

    def get_unread(self, receiver_id):
        try:
            return len(self.cache[receiver_id])
        except KeyError:
            return 0