from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, CharField, DateTimeField, dispatcher

@metamodelclass
@dispatcher
class Topic(ModelObject):
    tag: CharField(length=45, iskey=True)
    created: DateTimeField(iscomputed=True)