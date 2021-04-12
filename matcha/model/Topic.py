from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, DateTimeField

@dataclass(init=False)
class Topic(ModelObject):
    tag: CharField(length=45)
    created: DateTimeField(iscomputed=True)
