from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, IntField, DateTimeField, ArrayField, BoolField, dispatcher

@metamodelclass
@dispatcher
class Room(ModelObject):
    id: IntField(iskey=True,  iscomputed=True)
    users_ids: ArrayField(arraytype=int, length=2)
    active: BoolField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
