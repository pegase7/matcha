import json
from pathlib import Path
import logging
from logging import FileHandler
from datetime import datetime, date
import decimal
from matcha.orm.reflection import ModelObject

'''
Encoder used when deserializing for communication with JavaScript 
'''


class FlaskEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ModelObject):
            return o.__dict__
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Config():
    __instance = None
    """
    Check for singleton
    """

    def __new__(cls, basepath=None, configpath=None):
        """
        if previous instance is null instantiate and connect to database, elsewhere return current instance        
        """
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)
        return Config.__instance
    
    def __init__(self, basepath=None, configpath=None):
        if not hasattr(self, "basepath"): #self.basepath is Null only on the first pass 
            if basepath:
                self.basepath = basepath
            else:
                self.basepath = Path(__file__).parent.parent
                if 'src' == self.basepath.name:
                    self.basepath = self.basepath.parent
            if not configpath:
                configpath = 'resources/configuration/config.json'
            with open(self.basepath.joinpath(configpath), 'r') as f:
                self.config = json.load(f)
                if 'logging' in self.config:
                    self.configLogging()
            Config.__instance = self
            
    def configLogging(self):
        jsonlogging = self.config['logging']
        logginglevel = jsonlogging['level'] if 'level' in jsonlogging.keys() else 20
        loggingformat = jsonlogging['format'] if 'format' in jsonlogging.keys() else '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(lineno)d] %(message)s'
        loggingdatefmt = jsonlogging['dateFormat'] if 'dateFormat' in jsonlogging.keys() else '%Y-%m-%d:%H:%M:%S'
        
        logging.basicConfig(format=loggingformat, datefmt=loggingdatefmt, level=logginglevel)

        jsonloggers = jsonlogging['loggers'] if 'loggers' in jsonlogging else { "loggers":[{}] }
        for jsonlogger in jsonloggers:
            if "name" in jsonlogger.keys():
                __logger = logging.getLogger(jsonlogger["name"])
            else:
                __logger = logging.getLogger()
            if 'level' in jsonlogger:
                __logger.setLevel(jsonlogger['level'])

            if "file_error" in jsonlogger.keys():
                errorpath = self.basepath.joinpath(jsonlogger["file_error"])
                if not errorpath.parent.exists():
                    errorpath.parent.mkdir()
                error_fh = FileHandler(str(errorpath))
                __logger.addHandler(error_fh)
                error_fh.setFormatter(logging.Formatter(loggingformat))
                error_fh.setLevel(logging.ERROR)
    
