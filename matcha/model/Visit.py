from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, BoolField, ManyToOneField, dispatcher

@dataclass(init=False)
@dispatcher
class Visit(ModelObject):
  id: IntField(iskey=True)
  visited_id: ManyToOneField(modelname='Users')
  visitor_id: ManyToOneField(modelname='Users')
  visits_number: IntField()
  islike: BoolField()
  isblocked: BoolField()
  created: DateTimeField(iscomputed=True)
  last_update: DateTimeField(iscomputed=True)
  isfake: BoolField()
