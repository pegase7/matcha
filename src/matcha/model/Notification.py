from dataclasses import dataclass
from matcha.orm.reflection import metamodelclass, ModelObject, DateTimeField, IntField, ManyToOneField, EnumField, BoolField, dispatcher

@metamodelclass
@dispatcher
class Notification(ModelObject):
	id: IntField(iskey=True,  iscomputed=True)
	sender_id: ManyToOneField(modelname='Users')
	receiver_id: ManyToOneField(modelname='Users')
	notif_type: EnumField(values=['Like', 'Visit', 'Message', 'Like_too', 'Dislike'])
	is_read: BoolField()
	created: DateTimeField(iscomputed=True)