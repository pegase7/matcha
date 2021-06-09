import json
from pathlib import Path
import logging
from logging import FileHandler

'''
--------------------
EXAMPLE of json file
--------------------
{
    "postgresql":{
        "host":"localhost",
        "database":"matchadb",
        "user":"matchaadmin",
        "password":"bWF0Y2hhcGFzc3NhbGFnZW1hdGNoYXBhc3M=",
        "loggingConnection":"sql"
    },
    "logging":{
        "level":10,
        "format": "%(asctime)-19s,%(msecs)-4d %(levelname)-8s [%(module)-15s:%(lineno)-3d] %(message)s"
        "dateFormat":"%Y-%m-%d:%H:%M:%S", 
        "handlers": [
            { "logger_file":"resources/traces/standard_error.log" },
            { "name":"sql", "logger_file":"resources/traces/sql.log", "level":10 }
        ]
    },
    "recommendation":{
        "threshold":80,
        "nb_recommendations":80
    },
    "orm":{
        "raise_error":false,
        "logging_info":false,
        "logging_error":true
    }
}
------------
EXPLANATIONS
------------
    1) postgresql module:
        - host, database, user and password items determine connection parameters
        - loggingConnection item gives the name of the handler used for storing sql orders.
          If item value is null, standard logger is used. level must be equal to DEBUG (10).
          If loggingConnection module is present, sql order are displayed on standard logger (console)
    2) logging module:
        - level item determines logging level (i.e.: DEBUG, INFO, WARNING, ERROR, 10 means DEBUG).
        - format item: output format. default value is "%(asctime)-19s,%(msecs)-4d %(levelname)-8s [%(module)-15s:%(lineno)-3d] %(message)s".
        - dateformat item: Format of the date
        - handlers module:
          Different handlers can optionnally set. if name hamdler is null, default logger is assumed elsewhere a new logger is created.
    3) recommendation module:
        - threshold item: value giving the minimum of weighting needed to be selected.
        - nb_recommendations item: Maximum number of active recommendations for a user.
    4) orm module:
        specify what to do when error occurs on field checking: raise_error stop program, logging_error 
'''

class Config():
    __instance = None
    ''' Default values '''
    RAISE_ERROR = False
    LOGGING_INFO = False
    LOGGING_ERROR = True
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
            ormoptions = Config().config['orm']
            if ormoptions:
                if ormoptions['raise_error']:
                    Config.RAISE_ERROR = True if ormoptions['raise_error'] == True else False
                else:
                    Config.RAISE_ERROR = False
                if ormoptions['logging_info']:
                    Config.LOGGING_INFO = True if ormoptions['logging_info'] == True else False
                else:
                    Config.LOGGING_INFO = False
                if not ormoptions['logging_error'] is None: 
                    Config.LOGGING_ERROR = False if ormoptions['logging_error'] == False else True
                else:
                    Config.LOGGING_ERROR = True
            
    def configLogging(self):
        jsonlogging = self.config['logging']
        logginglevel = jsonlogging['level'] if 'level' in jsonlogging.keys() else 20
        loggingformat = jsonlogging['format'] if 'format' in jsonlogging.keys() else '%(asctime)-19s,%(msecs)-4d %(levelname)-8s [%(module)-15s:%(lineno)-3d] %(message)s'
        loggingdatefmt = jsonlogging['dateFormat'] if 'dateFormat' in jsonlogging.keys() else '%Y-%m-%d:%H:%M:%S'
        
        logging.basicConfig(format=loggingformat, datefmt=loggingdatefmt, level=logginglevel)

        jsonhandlers = jsonlogging['handlers'] if 'handlers' in jsonlogging else { "handlers":[{}] }
        for jsonhandler in jsonhandlers:
            if "name" in jsonhandler.keys():
                __logger = logging.getLogger(jsonhandler["name"])
            else:
                __logger = logging.getLogger()
            level = logging.ERROR
            if 'level' in jsonhandler:
                level = jsonhandler['level']
                __logger.setLevel(level)

            if "logger_file" in jsonhandler.keys():
                errorpath = self.basepath.joinpath(jsonhandler["logger_file"])
                if not errorpath.parent.exists():
                    errorpath.parent.mkdir()
                error_fh = FileHandler(str(errorpath))
                __logger.addHandler(error_fh)
                error_fh.setFormatter(logging.Formatter(loggingformat))
                error_fh.setLevel(level)
    
