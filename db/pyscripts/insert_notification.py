from matcha.orm.data_access import DataAccess
import random
from datetime import timedelta
from matcha.orm.reflection import ModelDict
from matcha.model.Notification import Notification
from matcha.model.Room import Room
from matcha.model.Message import Message
from faker import Faker

DATA_ACCESS = None

def insert_notification(sender_id, receiver_id, notif_type, created, is_read=False):
    notification = Notification()
    notification.sender_id = sender_id
    notification.receiver_id = receiver_id
    notification.notif_type = notif_type
    notification.is_read = is_read
    notification.created = created
    DATA_ACCESS.persist(notification)
    
def populate():
    global DATA_ACCESS
    DATA_ACCESS = DataAccess()

    # Change 'created' field so that it is no longer computed and can be set in this module 
    notificationmodel = ModelDict().get_model_class('Users')
    notificationmodel.get_field('created').iscomputed = False
    
    roommodel = ModelDict().get_model_class('Room')
    roommodel.get_field('created').iscomputed = False
    roommodel.get_field('last_update').iscomputed = False
 
    messagemodel = ModelDict().get_model_class('Users')
    messagemodel.get_field('created').iscomputed = False
    
    whereaddonstr = 'visited_id > visitor_id and (visited_id, visitor_id) in (select visitor_id, visited_id from visit where islike = true)'
    visits = DATA_ACCESS.fetch('Visit', conditions=[('islike', True)], whereaddon=(whereaddonstr,[]))
    expectedrooms = []
    for visit in visits:
        expectedrooms.append(str(visit.visited_id) + '_' + str(visit.visitor_id))
    deltas = []
    fake = Faker(['fr_CA'])
    for visit in visits:
        microseconds_between = (visit.last_update - visit.created).microseconds
        if 0 != microseconds_between:
            deltas = sorted(random.sample(range(0, microseconds_between), visit.visits_number))
        notif_type = 'Visit'
        hasreturnvisit = (str(visit.visited_id) + '_' + str(visit.visitor_id)) in expectedrooms and random.randint(0,5) > 0
        for i in range(visit.visits_number):
            if i == visit.visits_number - 1:
                created = visit.last_update + timedelta(milliseconds=1)
                if visit.isfake or visit.isblocked:
                    notif_type = 'Dislike'
                elif visit.islike:
                    notif_type = 'Like'
                    if hasreturnvisit:
                        room = Room()
                        room.users_ids = [visit.visited_id, visit.visitor_id]
                        room.created = created + timedelta(milliseconds=random.randint(12400000, 864000000))
                        room.active = random.randint(1, 7) != 1 
                        room.last_update = room.created
                        DATA_ACCESS.persist(room, autocommit=False)
                        nb_message = random.randint(0, 15)
                        is_read = True
                        created_message = room.created
                        for i in range(nb_message):
                            created_message = created_message + timedelta(milliseconds=random.randint(1240000, 86400000))
                            if nb_message - i <= 3 and is_read:
                                is_read = random.randint(1, 2) != 1
                            message = Message()
                            message.room_id = room.id
                            message.sender_id = visit.visited_id if random.randint(1, 2) != 1 else visit.visitor_id
                            message.created = created_message
                            nb_sentence = random.randint(1, 3)
                            chat = fake.sentence()
                            for _ in range(nb_sentence):
                                chat = chat + '\n' + fake.sentence()
                            message.chat = chat
                            receiver_id = visit.visited_id if message.sender_id == visit.visitor_id else visit.visitor_id
                            insert_notification(message.sender_id, receiver_id, 'Message', created_message, is_read)
                            DATA_ACCESS.persist(message, autocommit=False)
            else:
                created =  visit.created + timedelta(microseconds=deltas[i])  
            insert_notification(visit.visitor_id, visit.visited_id, notif_type, created)
                    
    DATA_ACCESS.commit()
            

                 
if '__main__' == __name__:
    populate()