from matcha.orm.reflection import ModelObject, metamodelclass, IntField, DateTimeField, ArrayField, BoolField,dispatcher

@dispatcher
@metamodelclass
class Room(ModelObject):
    id: IntField(iskey=True, iscomputed=True)
    users_ids: ArrayField(arraytype=int, length=2)
    active: BoolField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)