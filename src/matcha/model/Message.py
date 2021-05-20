from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, ManyToOneField, IntField, DateTimeField, TextField, dispatcher

@metamodelclass
@dispatcher
class Message(ModelObject):
    id: IntField(iskey=True, iscomputed=True)
    room_id: ManyToOneField(modelname='Room')
    sender_id: ManyToOneField(modelname='Users')
    chat: TextField()
    created: DateTimeField(iscomputed=True)