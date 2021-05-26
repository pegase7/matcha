
from matcha.orm.reflection import ModelObject, metamodelclass, ManyToOneField, dispatcher

@dispatcher
@metamodelclass
class Users_topic(ModelObject):
    users_id: ManyToOneField(modelname='Users', iskey=True)
    tag: ManyToOneField(modelname='Topic', iskey=True)
