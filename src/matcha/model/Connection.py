from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, CharField, IntField, DateTimeField, ManyToOneField, dispatcher

@metamodelclass
@dispatcher
class Connection(ModelObject):
    id: IntField(iskey=True,  iscomputed=True)
    users_id: ManyToOneField(modelname='Users')
    ip: CharField()
    connect_date: DateTimeField()
    disconnect_date: DateTimeField()
