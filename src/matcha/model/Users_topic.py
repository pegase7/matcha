from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, ManyToOneField, dispatcher

@metamodelclass
@dispatcher
class Users_topic(ModelObject):
    users_id: ManyToOneField(modelname='Users')
    tag: ManyToOneField(modelname='Topic')
