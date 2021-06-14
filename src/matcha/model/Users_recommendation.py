from matcha.orm.reflection import ModelObject, metamodelclass, IntField, FloatField, DateTimeField, ManyToOneField, BoolField, dispatcher, ListField

@dispatcher
@metamodelclass
class Users_recommendation(ModelObject):
    id: IntField(iskey=True, iscomputed=True)
    sender_id: ManyToOneField(modelname='Users')
    receiver_id: ManyToOneField(modelname='Users')
    weighting: IntField()
    age_diff: IntField()
    age_ratio: IntField()
    distance: FloatField()
    dist_ratio: IntField()
    topics_ratio: FloatField()
    is_rejected: BoolField()
    last_consult: DateTimeField(iscomputed=True)
    created: DateTimeField(iscomputed=True)
    last_update: DateTimeField(iscomputed=True)
    topics: ListField(modelname='Recommendation_topic', select='select * from Recommendation_topic where recommend_id = %s order by tag')
