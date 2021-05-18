from matcha.orm.reflection import ModelObject, metamodelclass, IntField, FloatField, DateTimeField, ManyToOneField, BoolField, dispatcher

@dispatcher
@metamodelclass
class Users_recommendation(ModelObject):
    id: IntField(iskey=True, iscomputed=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    age_diff: FloatField()
    distance: FloatField()
    dist_ratio: IntField()
    topics_ratio: FloatField()
    is_rejected: BoolField()
    last_consult: DateTimeField(iscomputed=True)
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
