from datetime import datetime
import re
import importlib
import dataclasses

class Field:
    
    def __init__(self, iscomputed=False, iskey=False):
        self.value = None
        self.iscomputed = iscomputed
        self.iskey = iskey
    
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = value

class IntField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        super().__set__(instance, value)

class CharField(Field):
    def __init__(self, iscomputed=False, iskey=False, length=None):
        Field.__init__(self, iscomputed, iskey)
        self.length = length
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        if len(value) > self.length:
            raise ValueError("Maximum length('"+ self.length + ") is exceeded by value '" + value + "'!")
        super().__set__(instance, value)

class TextField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        super().__set__(instance, value)

class EmailField(Field):
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(instance, self._name, str, value)
        if not re.search("'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'", value):
            raise ValueError("''" + "is not a valid email!")
        super().__set__(instance, value)

class EnumField(Field):

    def __init__(self, iscomputed=False, iskey=False, values=[]):
        Field.__init__(self, iscomputed, iskey)
        self.values = values
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(instance, self._name, int, value)
        if value not in self.values:
            raise ValueError("'" + value + "' is not a authorized value for enum '"+ self.values + "'!'" )
        super().__set__(instance, value)

class FloatField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise TypeError(instance, self._name, int, value)
        super().__set__(instance, value)

class BoolField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise TypeError(instance, self._name, bool, value)
        super().__set__(instance, value)

class DateField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise TypeError(instance, self._name, datetime, value)
        super().__set__(instance, datetime.datetime(value.year, value.month, value.day))

class DateTimeField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, datetime):
            raise TypeError(instance, self._name, datetime, value)
        super().__set__(instance, value)

class ArrayField(Field):

    def __init__(self, iscomputed=False, iskey=False, arraytype=None, length=None):
        Field.__init__(self, iscomputed, iskey)
        self.arraytype = arraytype
        self.length = length
    
    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError(instance, self._name, list, value)
            if not self.arraytype is None:
                for i in value:
                    if not isinstance(i, int):
                        raise TypeError(instance, self._name, self.arraytype, value)
        if not self.length is None and len(value) != self.length:
            raise ValueError("Invalid number of elements'"+ self.length + "!")            
        super().__set__(instance, value)

class ManyToOneField(Field):
    def __init__(self, iscomputed=False, iskey=False, modelname=None):
        Field.__init__(self, iscomputed, iskey)
        if modelname is None is None:
            raise ValueError("'modelname' attribute must be specified!")
        self.modelname = modelname
    def __set__(self, instance, value):
        self.value = value

class ListField(Field):
    def __init__(self, iscomputed=False, iskey=False, modelname=None, select=None):
        if modelname is None or select is None:
            raise ValueError("'modelname' and 'select' attributes must be specified!")
        Field.__init__(self, iscomputed, iskey)
        self.modelname = modelname
        self.select = select
    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise TypeError(instance, self._name, list, value)
        self.value = value

class ModelObject(object):
    @classmethod
    def get_model_name(cls):
        return cls.__name__
    
    def __str__(self):
        if self.id is None:
            return ModelObject.get_model_name() + " is None"
        else:
            model = ModelDict().get_model(self.get_model_name())
            return model.model_str(self) 

class Model():
    def __init__(self, model_name):
        self.fields = []
        self.dictfields = {}
        self.name = model_name
        self.klazz = self.get_class()
        self.key_field = None
        instance = self.new_instance()
        for field in dataclasses.fields(instance):
            self.fields.append(field)
            self.dictfields[field.name] = field
    
    def get_fields(self):
        return self.fields;

    def get_id(self, record):
        return getattr(record, self.get_key_field().name)

    def get_key_field(self):
        for field in self.fields:
            if field.type.iskey:
                self.key_field = field
                break
        return self.key_field;

    def get_field(self, field_name):
        try:
            return self.dictfields[field_name]
        except KeyError:
            raise ValueError("No field '" + field_name + "' for '" +self.name + "'!'")

    def new_instance(self):
        return eval("modelObject()", { "modelObject": self.klazz})
        
    def get_class(self):
        """
        Create a class instance from class '{class_name}' from module 'matcha.model.{class_name}'
        """
        try:
            module_path = "matcha.model." + self.name
            mod = importlib.import_module(module_path)
            return getattr(mod, self.name)
        except (ImportError, AttributeError):
            raise ImportError(self.name)
    
    def head(self, instance, model_name):
        head = model_name + "("
        delim = ''
        for field in self.fields:
            if field.type.iskey:
                head += delim + field.name + ': ' + str(getattr(instance, field.name))
                delim = ', '
        head += ")" 
        return head
        
    def model_str(self, instance):
#         head = self.name + "("
#         delim = ''
#         for field in self.fields:
#             if field.type.iskey:
#                 head += delim + field.name + ': ' + str(getattr(instance, field.name))
#                 delim = ', '
#         head += ")\n"
        model_str = self.head(instance, self.name)  + "\n"
        for field in self.fields:
            if not field.type.iskey and not isinstance(field.type, ListField):
                attr = getattr(instance, field.name)
                if hasattr(attr, 'get_model_name'):
                    attr = self.head(attr, type(attr).__name__)
                model_str += '    ' + field.name + ': ' + str(attr) + '\n'
        return model_str

    def pre_persist(self, record):
        pass

    def pre_merge(self, record):
        pass

    def pre_remove(self, record):
        pass

class ModelDict(object):
    """
    ModelDict est une classe singleton contenant dictionnaire (en cache) la liste des Objects
    et pour chaque objet la liste des champs.
    """
    __instance = None
    __models = {}
    def __new__(cls):
        if ModelDict.__instance is None:
            ModelDict.__instance = object.__new__(cls)
        return ModelDict.__instance

    
    def get_model(self, model_name:str):
        try:
            model = ModelDict.__models[model_name]
        except (KeyError):
            model = Model(model_name)
            ModelDict.__models[model_name] = model
        return model
    