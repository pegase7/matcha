from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField

@dataclass(init=False)
class Users_tag(ModelObject):
    users_id: ManyToOneField(iskey=True)
    tag_id: ManyToOneField(iskey=True)
