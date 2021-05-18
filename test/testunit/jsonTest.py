import unittest
import json
import logging
from matcha.orm.data_access import DataAccess
from matcha.orm.reflection import dispatcher, ModelDict, Field, ListField

class JsonTestCase(unittest.TestCase):

    def runTest(self):
        print("\n")
        logging.info('   +-----------+')
        logging.info('   | Test JSON |')
        logging.info('   +-----------+')
        self.test_model('Users')
        self.test_model('Connection')
        self.test_model('Room')
        self.test_model('Topic')
        self.test_model('Visit')

    def test_model(self, modelname):
        result = DataAccess().fetch(modelname)
        modelclass = ModelDict().get_model_class(modelname)
        keyfieldname =modelclass.get_key_field().name
        obj_id = ' ' + keyfieldname + ':'
        for obj in result:
            self.test_serialization(obj, modelname + obj_id + str(getattr(obj, keyfieldname)))
        
    def test_serialization(self, model_object, obj_id ):
        self.assertIsNotNone(model_object, obj_id+ '  not found')
        serial_object = json.dumps(model_object, default=dispatcher.encoder_default) #Serialization
        deserial_object = json.loads(serial_object, object_hook=dispatcher.decoder_hook) #Deserialization
        self.assertEqual(type(model_object), type(deserial_object), 'Different types for '+ obj_id)
        modelclass = ModelDict().get_model_class(deserial_object.get_model_name())
        for field in modelclass.get_fields():
            if isinstance(field, Field) and not isinstance(field, ListField):
                value1 = getattr(model_object, field.name)
                value2 = getattr(deserial_object, field.name)
                self.assertEqual(value1, value2, "for field '" + field.name + "' for " + obj_id)
        logging.info('Json test ok for ' + obj_id)
