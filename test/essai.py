from bisect import bisect

class Field(object):
    # A global creation counter that will contain the number of Field objects
    # created globally.
    creation_counter = 0

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        # Store the creation index in the "creation_counter" of the field.
        self.creation_counter = Field.creation_counter
        # Increment the global counter.
        Field.creation_counter += 1
        # As with Django, we'll be storing the name of the model property
        # that holds this field in "name".
        self.name = None
    
    def __get__(self, obj, owner):
        # return obj._data[self._name]
        return self.value

    def __set__(self, obj, value):
        self.value = value
        print('set')
        # obj._data[self._name] = value

        

    def __cmp__(self, other):
        # This specifies that fields should be compared based on their creation
        # counters, allowing sorted lists to be built using bisect.
        if self.creation_counter == other.creation_counter:
            return 0
        elif self.creation_counter > other.creation_counter:
            return 1
        else:
            return -1

# A metaclass used by all Models
class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        klass = super(ModelBase, cls).__new__(cls, name, bases, attrs)
        fields = []
        # Add all fields defined for the model into "fields".
        for key, value in attrs.items():
            if isinstance(value, Field):
                # Store the name of the model property.
                value.name = key
                # This ensures the list is sorted based on the creation order
                fields.insert(bisect(fields, value), value)
        # In Django, "_meta" is an "Options" object and contains both a
        # "local_fields" and a "many_to_many_fields" property. We'll use a
        # dictionary with a "fields" key to keep things simple.
        klass._meta = { 'fields': fields }
        return klass

class Model(object):
    __metaclass__ = ModelBase

class Model1(Model):
    a: Field()
    b: Field()
    c = Field()
    z = Field()

class Model2(Model):
    c = Field()
    z = Field()
    b = Field()
    a = Field()

if __name__ == "__main__":
    model10 = Model1()
    model10.a = 'a'
    model11 = Model1()
    model11.a = 'b '
    print(model10.a, model11.a)