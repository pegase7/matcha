from dataclasses import dataclass
from matcha.orm.reflection import ModelObject, IntField, DateTimeField, ManyToOneField, EnumField

@dataclass(init=False)
class Visit(ModelObject):
    id: IntField(iskey=True)
    users_id: ManyToOneField(modelname='Users')
    position: EnumField(values=['Like', 'Unlike'])
    connect_date: DateTimeField()
    disconnect_date: DateTimeField()
