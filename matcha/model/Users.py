from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, IntField, DateField, DateTimeField, EmailField, BoolField, EnumField, TextField, ListField, FloatField

@dataclass(init=False)
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
    orientation: EnumField(values=['Hetero', 'Homo', 'bi'])
    birthday: DateField()
    latitude: FloatField()
    longitude: FloatField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
    connections: ListField(modelname='Connection', select='select * from CONNECTION where users_id = %s order by id')
    topics: ListField(modelname='Topic', select='select T.* from USERS_TOPIC as UT  left outer join TOPIC as T on T.id = UT.tag_id where users_id = %s order by T.id')
    rooms: ListField(modelname='Room', select='select R.* from USERS_ROOM as UR  left outer join ROOM as R on R.id = UR.room_id where master_id = %s order by R.id')
