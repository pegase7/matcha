from matcha.orm.reflection import ModelObject, metamodelclass, DateTimeField, IntField, ManyToOneField, EnumField, BoolField, dispatcher

@dispatcher
@metamodelclass
class Notification(ModelObject):
    id: IntField(iskey=True, iscomputed=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    notif_type: EnumField(values=['Like', 'Visit', 'Message', 'Like_too', 'Dislike'])
    is_read: BoolField()
    created: DateTimeField(iscomputed=True)