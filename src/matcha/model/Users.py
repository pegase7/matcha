from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, CharField, IntField, DateField, DateTimeField, EmailField, BoolField, EnumField, TextField, ListField, FloatField, dispatcher

@metamodelclass
@dispatcher
class Users(ModelObject):
    id: IntField(iskey=True)
    first_name: CharField(length=45)
    last_name: CharField(length=45)
    user_name: CharField(length=45)
    password: CharField(length=45)
    description: TextField()
    email: EmailField()
    active: BoolField()
    confirm: CharField(length=20)
    gender: EnumField(values=['Male', 'Female'])
    orientation: EnumField(values=['Hetero', 'Homo', 'Bi'])
    birthday: DateField()
    latitude: FloatField()
    longitude: FloatField()
    popularity: IntField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
    connections: ListField(modelname='Connection', select='select * from CONNECTION where users_id = %s order by id')
    topics: ListField(modelname='Topic', select='select T.* from USERS_TOPIC as UT  left outer join TOPIC as T on T.tag = UT.tag where users_id = %s order by T.tag')
    rooms: ListField(modelname='Room', select='select R.* from USERS_ROOM as UR  left outer join ROOM as R on R.id = UR.room_id where master_id = %s order by R.id')
    asvisiteds: ListField(modelname='Visit', select='select V.* from VISIT as V where visited_id = %s order by v.last_update')
    asvisitors: ListField(modelname='Visit', select='select V.* from VISIT as V where visitor_id = %s order by v.last_update')
    messages: ListField(modelname='Message', select='select M.* from MESSAGE as M where sender_id = %s order by M.created')
# 
#     def __init__(self):
#         self.connections = []
#         self.topics = []
#         self.rooms = []