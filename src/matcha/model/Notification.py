from matcha.orm.reflection import ModelObject, metamodelclass, DateTimeField, IntField, ManyToOneField, EnumField, BoolField, dispatcher

@dispatcher
@metamodelclass
class Notification(ModelObject):
    id: IntField(iskey=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    notif_type: EnumField(values=['Like', 'Visit', 'Message', 'Like_too', 'Dislike'])
    read_notif: BoolField()
    created: DateTimeField(iscomputed=True)
