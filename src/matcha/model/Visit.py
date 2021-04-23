from matcha.orm.reflection import ModelObject, metamodelclass, IntField, DateTimeField, BoolField, ManyToOneField, dispatcher

@dispatcher
@metamodelclass
class Visit(ModelObject):
    id = IntField(iskey=True)
    visited_id = ManyToOneField(modelname='Users')
    visitor_id = ManyToOneField(modelname='Users')
    visits_number = IntField()
    islike = BoolField()
    isblocked = BoolField()
    created = DateTimeField(iscomputed=True)
    last_update = DateTimeField(iscomputed=True)
