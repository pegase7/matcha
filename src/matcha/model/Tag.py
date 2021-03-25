from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, CharField, IntField

@dataclass(init=False)
class Tag(ModelObject):
    id: IntField(iskey=True)
    wording: CharField(length=45)
