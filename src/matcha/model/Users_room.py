from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, ManyToOneField, dispatcher

@metamodelclass
@dispatcher
class Users_room(ModelObject):
    room_id: ManyToOneField(modelname='Room', iskey=True)
    master_id: ManyToOneField(modelname='Users', iskey=True)
    slave_id: ManyToOneField(modelname='Users')
