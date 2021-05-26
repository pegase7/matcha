# import json
# from pathlib import Path

# basepath = Path(__file__).parent.parent
# if 'src' == basepath.name:
#     basepath = basepath.parent
# basepath = basepath.joinpath('resources/configuration/config.json')
# with open(basepath, 'r') as f:
#     config = json.load(f)
# print('Configuration:', config['postgresql'])

###########################################
import json
from pathlib import Path
import logging
from logging import FileHandler

print("Import Config")


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