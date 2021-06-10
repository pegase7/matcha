from datetime import datetime, date
from decimal import Decimal
import re
import importlib
import logging
from matcha.config import Config

'''

        F I E L D S
        -----------

'''
class Field:

    def __init__(self, iscomputed=False, iskey=False):
        self.value = None
        self.iscomputed = iscomputed
        self.iskey = iskey
    
    def check(self, instance, value):
        return value
    
    def __msgerror__(self, value, message, instance=None):
        if not instance is None:
            instance.haserror=True
        return "value '" + str(value) + "' for field '" + self.name + "' " + message

    def __msgtypeerror__(self, value, _type, instance=None):
        return self.__msgerror__(value, self.name, "bad type, '" + _type + "' is expected rather than '" + str(type(value)) + "'!", instance)
    
    def __raise_error__(self, error, message):
        if Config.LOGGING_INFO:
            logging.info(message)
        if Config.LOGGING_ERROR:
            logging.error(message)
        if Config.RAISE_ERROR:
            if error:
                raise error
            else:
                raise Exception(message)
 

class IntField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def check(self, instance, value):
        if not value is None: #Don't forget if value==0, return false
            try:
                if isinstance(value, str):
                    return int(value)
            except ValueError:
                self.__raise_error__( TypeError(instance, self.name, int, value), "Type Error on field '" + self.name + "' for value:" + value)
            if isinstance(value, Decimal):
                value = int(value)
            elif not isinstance(value, int):
                self.__raise_error__( TypeError(instance, self.name, int, value), "Type Error on field '" + self.name + "' for value:" + value)
        return value


class CharField(Field):

    def __init__(self, iscomputed=False, iskey=False, length=None):
        Field.__init__(self, iscomputed, iskey)
        self.length = length
    
    def check(self, instance, value):
        if value and not isinstance(value, str):
            logging.error(self.__msgtypeerror__(value, 'str', instance))
        if value and self.length and len(value) > self.length:
            logging.error(self.__msgerror__(value, "Maximum length('" + self.length + ") is exceeded!", instance))
        return value


class TextField(Field):

    def check(self, instance, value):
        if value and not isinstance(value, str):
            logging.error(self.__msgtypeerror__(value, 'str', instance))
        return value


class EmailField(Field):
    
    def check(self, instance, value):
        if not isinstance(value, str):
            logging.error(self.__msgtypeerror__(value, 'str', instance))
        elif not re.search("^[^@]+@[^@]+\.[^@]+$", value):
            logging.error(self.__msgerror__(value, "is not a valid email!", instance))
        return value


class EnumField(Field):

    def __init__(self, iscomputed=False, iskey=False, values=[]):
        Field.__init__(self, iscomputed, iskey)
        self.values = values
    
    def check(self, instance, value):
        if value and value not in self.values:
            logging.error(self.__msgerror__(value, " is not a authorized value for enum!", instance))
        return value


class FloatField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def check(self, instance, value):
        if not value is None: #Don't forget if value==0, return false
            try:
                if isinstance(value, str):
                    return float(value)
            except ValueError:
                self.__raise_error__( TypeError(instance, float.name, int, value), "Type Error on field '" + self.name + "' for value:" + value)
            if isinstance(value, Decimal):
                value = float(value)
            elif not isinstance(value, float):
                logging.error(self.__msgtypeerror__(value, 'float', instance))
        return value


class BoolField(Field):

    def __init__(self, iscomputed=False, iskey=False):
        Field.__init__(self, iscomputed, iskey)
    
    def check(self, instance, value):
        try:
            if isinstance(value, str):
                return bool(value)
        except ValueError:
            self.__raise_error__( TypeError(instance, self.name, bool, value), "Type Error on field '" + self.name + "' for value:" + value)
        if value and not isinstance(value, bool):
            logging.error(self.__msgtypeerror__(value, 'bool', instance))
        return value


class DateField(Field):

    def check(self, instance, value):
        try:
            if isinstance(value, str):
                return date.fromisoformat(value)
            elif isinstance(value, datetime):
                return datetime.date(value.year, value.month, value.day)
            else:
                if value and not isinstance(value, date):
                    logging.error(self.__msgtypeerror__(value, 'date', instance))
        except ValueError:
            logging.error(self.__msgtypeerror__(value, 'date', instance))
        return value

class DateTimeField(Field):

    def check(self, instance, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                logging.error(self.__msgtypeerror__(value, 'datetime', instance))
                return value
        else:
            if value and not isinstance(value, datetime):
                logging.error(self.__msgtypeerror__(value, 'datetime', instance))
        return value


class ArrayField(Field):

    def __init__(self, iscomputed=False, iskey=False, arraytype=None, length=None):
        Field.__init__(self, iscomputed, iskey)
        self.arraytype = arraytype
        self.length = length
    
    def check(self, instance, value):
        if not isinstance(value, list):
            logging.error(self.__msgtypeerror__(value, 'list', instance))
            if not self.arraytype is None:
                for i in value:
                    if not isinstance(i, int):
                        logging.error(self.__typee(value, self.name, str(self.arraytype)))
        if not self.length is None and len(value) != self.length:
            logging.error(self.__msgerror__(value, "Invalid number of elements'" + self.length + "!", instance))
        return value


class ManyToOneField(Field):

    def __init__(self, iscomputed=False, iskey=False, modelname=None):
        Field.__init__(self, iscomputed, iskey)
        if modelname is None:
            logging.error(self.__msgerror__(None, "'modelname' attribute must be specified!"))
        else:
            self.modelname = modelname


class ListField(Field):

    def __init__(self, iscomputed=False, iskey=False, modelname=None, select=None):
        if modelname is None or select is None:
            logging.error(self.__msgerror__(None, "'modelname' and 'select' attributes must be specified!"))
        Field.__init__(self, iscomputed, iskey)
        self.modelname = modelname
        self.select = select
        self.value = []

    def check(self, instance, value):
        if not isinstance(value, list):
            logging.error(self.__msgtypeerror__(value, 'list', instance))
        return value


class ModelObject(object):
    '''
    Parent class for all model object.
    '''

    @classmethod
    def get_model_name(cls):
        return cls.__name__

    def __init__(self):
        self.haserror = False
        
    def _as_dict(self):
        __dict = {}
        modelclass = ModelDict().get_model_class(self.get_model_name())
        for field in modelclass.get_fields():
            if hasattr(self, field.name):
                __dict[field.name] = getattr(self, field.name)
        return __dict

    def __str__(self):
        model = ModelDict().get_model_class(self.get_model_name())
        return model.model_str(self)

    def check(self):
        self.haserror = False
        modelclass = ModelDict().get_model_class(self.get_model_name())
        for field in modelclass.get_fields():
            if not isinstance(field, ListField):
                field.check(self, getattr(self, field.name))
        return self.haserror
    
'''

        M E T A - D I C T I O N A R Y
        -----------------------------

'''
class ModelClass():

    def __init__(self, cls_, name, fields, dictfields):
        self.fields = fields
        self.dictfields = dictfields
        self.name = name
        self.klazz = cls_
        self.key_field = None
        ModelDict().add_modelClass(name, self)
    
    def get_fields(self):
        return self.fields;

    def get_id(self, record):
        return getattr(record, self.get_key_field().name)

    def get_key_field(self):
        for field in self.fields:
            if field.iskey:
                self.key_field = field
                break
        return self.key_field;

    def get_field(self, field_name):
        try:
            return self.dictfields[field_name]
        except KeyError:
            raise ValueError("No field '" + field_name + "' for '" + self.name + "'!'")

    def new_instance(self):
        return eval("ModelObject()", { "ModelObject": self.klazz})

    def head(self, instance, model_name):
        head = model_name + "("
        delim = ''
        for field in self.fields:
            if hasattr(instance, field.name)  and field.iskey:
                head += delim + field.name + ': ' + str(getattr(instance, field.name))
                delim = ', '
        head += ")" 
        return head
        
    def model_str(self, instance):
        model_str = self.head(instance, self.name) + "\n"
        for field in self.fields:
            if not field.iskey and not isinstance(field, ListField) and hasattr(instance, field.name):
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
    ModelDict is a SINGLETON class containing a dictonary {modek_name, ModelClass}, instance of ModelClass containing needed information on fields 
    """
    __instance = None
    __models = {}

    def __new__(cls):
        if ModelDict.__instance is None:
            ModelDict.__instance = object.__new__(cls)
        return ModelDict.__instance
    
    def add_modelClass(self, name:str, modelClass):
        ModelDict.__models[name] = modelClass
        
    def get_model_class(self, model_name:str):
        '''
        Generally, model class is already present inside dictionary because dictionary are populated during first model class call.
        However, item can be missing e.g. when building ListField because dictionary information are required before instantiation. 
        '''
        try:
            return ModelDict.__models[model_name]
        except (KeyError):
            self.__instantiate(model_name)
            return ModelDict.__models[model_name]

    def __instantiate(self, name):
        """
        Create a class instance from class '{class_name}' from module 'matcho.model.{class_name}'
        """
        try:
            module_path = "matcha.model." + name
            mod = importlib.import_module(module_path)
            eval("ModelObject()", { "ModelObject": getattr(mod, name)})
        except (ImportError, AttributeError):
            raise ImportError(name)



'''

        D E C O R A T O R S
        -------------------

'''

'''
function decorator launch when calling model class for the first time.
'''        
def metamodelclass(cls=None):

    def wrap(cls):
        fields = []
        dictfield = {}
        
        cls_annotations = cls.__dict__.get('__annotations__', {})
        for name, field in cls_annotations.items():
            if isinstance(field,Field):
                field.name = name
                fields.append(field)
                dictfield[name] = field
        ModelClass(cls, cls.__name__, fields, dictfield)
        return cls

    return wrap(cls)


'''
class Dispatcher is a decorator use on Model Instance in order to assume serialization and deserialization
'''   
class _Dispatcher:

    def __init__(self, classname_key='__class__'):
        self._key = classname_key
        self._classes = {}  # to keep a reference to the classes used

    def __call__(self, class_):  # decorate a class
        self._classes[class_.__name__] = class_
        return class_

    def decoder_hook(self, d):
        classname = d.pop(self._key, None)
        modelclass = ModelDict().get_model_class(classname)
        if classname:
            if modelclass:
                for field in modelclass.get_fields():
                    if isinstance(field, DateTimeField):
                        dt = d[field.name]
                        if dt:
                            d[field.name] = datetime.fromisoformat(dt)
                    elif isinstance(field, DateField):
                        dt = d[field.name]
                        if dt:
                            d[field.name] = date.fromisoformat(dt)
            obj = self._classes[classname]()
            for name, value in d.items():
                setattr(obj, name, value)
        return obj

    def encoder_default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return str(obj)
        d = obj._as_dict()
        d[self._key] = type(obj).__name__
        return d


dispatcher = _Dispatcher()
