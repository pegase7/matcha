from flask import Flask
from matcha.model.Notification import Notification 
from matcha.orm.data_access import DataAccess


def find_notif_list(us_id):
        notif_list = DataAccess().fetch('Notification', conditions=[('receiver_id', us_id), 
                                                                    ('read_notif', False),
                                                                    ('notif_type', 'Message')
                                                                    ])
        return notif_list
