from matcha.orm.reflection import ModelObject, metamodelclass, ManyToOneField, IntField, DateTimeField, TextField, dispatcher

@dispatcher
@metamodelclass
class Message(ModelObject):
    id = IntField(iskey=True)
    room_id = ManyToOneField(modelname='Room')
    sender_id = ManyToOneField(modelname='Users')
    chat = TextField()
    created = DateTimeField(iscomputed=True)