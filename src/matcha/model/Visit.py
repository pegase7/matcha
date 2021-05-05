from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ManyToOneField, BoolField, dispatcher

@dataclass(init=False)
@dispatcher
class Visit(ModelObject):
    id: IntField(iskey=True)
    visited_id: ManyToOneField(modelname='Users')
    visitor_id: ManyToOneField(modelname='Users')
    islike: BoolField()
    isblocked: BoolField()
    visits_number: IntField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
