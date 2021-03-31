from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, ManyToOneField

@dataclass(init=False)
class Users_room(ModelObject):
    room_id: ManyToOneField(modelname='Room')
    master_id: ManyToOneField(modelname='Users')
    slave_id: ManyToOneField(modelname='Users')
