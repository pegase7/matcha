from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField, IntField, DateTimeField, TextField, dispatcher

@dataclass(init=False)
@dispatcher
class Message(ModelObject):
    id: IntField(iskey=True)
    room_id: ManyToOneField(modelname='Room')
    sender_id: ManyToOneField(modelname='Users')
    chat: TextField()
    created: DateTimeField(iscomputed=True)
