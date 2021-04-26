from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ArrayField, BoolField, dispatcher

@dataclass(init=False)
@dispatcher
class Room(ModelObject):
    id: IntField(iskey=True)
    users_ids: ArrayField(arraytype=int, length=2)
    active: BoolField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
