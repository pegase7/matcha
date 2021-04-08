from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField

@dataclass(init=False)
class Users_topic(ModelObject):
    users_id: ManyToOneField(modelname='Users')
    tag: ManyToOneField(modelname='Tag')
