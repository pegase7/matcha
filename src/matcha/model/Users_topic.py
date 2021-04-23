from matcha.orm.reflection import ModelObject, metamodelclass, ManyToOneField, dispatcher

@dispatcher
@metamodelclass
class Users_topic(ModelObject):
    users_id = ManyToOneField(modelname='Users')
    tag = ManyToOneField(modelname='Tag')
