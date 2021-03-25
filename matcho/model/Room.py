from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ArrayField

@dataclass(init=False)
class Room(ModelObject):
    id: IntField(iskey=True)
    users_ids: ArrayField(arraytype=int, length=2)
    last_update: DateTimeField(iscomputed=True)
