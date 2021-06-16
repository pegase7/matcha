from matcha.orm.data_access import DataAccess
        
data_access = None

'''
Provides a way to work on a dict_users rather than on database when searching unread notifications for a users.
Otherwise, database would be queried every 5 seconds.
    - merge and persist on Notification must use NotificationCache functions instead of DataAccess functions.
    - get_unread gives numbers of unread notificationsß split in Like, Message, Visit, Dislike types for an User Id.
'''
class NotificationCache():
    
    def init(self):
        global data_access
        data_access = DataAccess()
        self.dict_user_names = {}
        # dict_users: Dict Users id, set of unread notification ids.
        self.dict_users = {}
        # dict_notification: Dict Notification,id, Notifications.
        self.dict_notification = {}
        notifications = data_access.fetch('Notification', ('is_read', False), joins='receiver_id')
        
        for notification in notifications:
            if not notification.receiver_id.user_name in self.dict_users:
                self.dict_users[notification.receiver_id.user_name] = set()
            self.dict_users[notification.receiver_id.user_name].add(notification.id)
            self.dict_notification[notification.id] = notification

    def merge(self, notification, autocommit=True):
        if notification.is_read:
            try:
                receiver_name = self.get_user_name(notification.receiver_id)
                notif_set = self.dict_users[receiver_name]
                notif_set.discard(notification.id)
                del self.dict_notification[notification.id]
            except KeyError:
                pass
        data_access.merge(notification, autocommit)

    def persist(self, notification, autocommit=True):
        global data_access
        data_access.persist(notification, autocommit)
        receiver_name = self.get_user_name(notification.receiver_id)
        if not receiver_name in self.dict_users:
            self.dict_users[receiver_name] = set()
        self.dict_users[receiver_name].add(notification.id)
        self.dict_notification[notification.id] = notification

    def get_unread(self, receiver_name):
        try:
            notificationids = self.dict_users[receiver_name]
            like = message = visit = dislike  = 0
            for notifid in notificationids:
                notification = self.dict_notification[notifid]
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

    def get_user_name(self, users_id):
        if users_id not in self.dict_user_names:
            users = data_access.find('Users', conditions=('id', users_id))
            self.dict_user_names[users_id] = users.user_name
            return users.user_name
        return self.dict_user_names[users_id]
    
