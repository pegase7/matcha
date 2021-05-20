from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, IntField, DateTimeField, ManyToOneField, BoolField, dispatcher

@metamodelclass
@dispatcher
class Visit(ModelObject):
    id: IntField(iskey=True, scomputed=True)
    visited_id: ManyToOneField(modelname='Users')
    visitor_id: ManyToOneField(modelname='Users')
    islike: BoolField()
    isblocked: BoolField()
    visits_number: IntField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
    isfake: BoolField()