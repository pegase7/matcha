from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ArrayField, BoolField

@dataclass(init=False)
class Room(ModelObject):
    id: IntField(iskey=True)
    users_ids: ArrayField(arraytype=int, length=2)
    active: BoolField()
    last_update: DateTimeField(iscomputed=True)
