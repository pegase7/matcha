from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField, IntField, DateTimeField, TextField

@dataclass(init=False)
class Message(ModelObject):
    id: IntField(iskey=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    chat: TextField()
    last_update: DateTimeField(iscomputed=True)