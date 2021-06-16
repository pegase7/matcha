from matcha.orm.reflection import ModelObject, metamodelclass, ManyToOneField, ListField, dispatcher

@dispatcher
@metamodelclass
class Recommendation_topic(ModelObject):
    recommend_id: ManyToOneField(modelname='Users_recommendation', iskey=True)
    tag: ManyToOneField(modelname='Topic', iskey=True)
