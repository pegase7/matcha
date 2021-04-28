from matcha.orm.reflection import ModelObject, metamodelclass, IntField, FloatField, DateTimeField, ManyToOneField, dispatcher

@dispatcher
@metamodelclass
class Users_recommandation(ModelObject):
    id: IntField(iskey=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    age_diff: FloatField()
    distance: FloatField()
    dist_ratio: IntField()
    topics_ratio: FloatField()
    last_consult: DateTimeField(iscomputed=True)
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
