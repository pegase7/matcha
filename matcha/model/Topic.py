from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, DateTimeField, dispatcher

@dataclass(init=False)
@dispatcher
class Topic(ModelObject):
    tag: CharField(length=45)
    created: DateTimeField(iscomputed=True)
