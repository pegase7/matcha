from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, IntField, DateTimeField, ManyToOneField, dispatcher

@dataclass(init=False)
@dispatcher
class Connection(ModelObject):
    id: IntField(iskey=True)
    users_id: ManyToOneField(modelname='Users')
    ip: CharField()
    connect_date: DateTimeField()
    disconnect_date: DateTimeField()
