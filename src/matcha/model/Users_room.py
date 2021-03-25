from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField

@dataclass(init=False)
class Users_room(ModelObject):
    users_id: ManyToOneField(modelname='Users')
    room_id: ManyToOneField(modelname='Users')
