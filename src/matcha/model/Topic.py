from matcha.orm.reflection import ModelObject, metamodelclass, CharField, DateTimeField, dispatcher

@dispatcher
@metamodelclass
class Topic(ModelObject):
    tag = CharField(length=45)
    created = DateTimeField(iscomputed=True)
