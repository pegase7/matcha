from matcha.orm.reflection import metamodelclass, ModelObject, CharField, IntField, DateTimeField, ManyToOneField, dispatcher

@dispatcher
@metamodelclass
class Connection(ModelObject):
    id = IntField(iskey=True)
    users_id = ManyToOneField(modelname='Users')
    ip = CharField()
    connect_date = DateTimeField()
    disconnect_date = DateTimeField()
