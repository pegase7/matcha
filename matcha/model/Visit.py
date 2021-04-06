from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ManyToOneField, BoolField

@dataclass(init=False)
class Visit(ModelObject):
    id: IntField(iskey=True)
    visited_id: ManyToOneField(modelname='Users')
    visitor_id: ManyToOneField(modelname='Users')
    is_like: BoolField
    visit_number: IntField()
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
