import json
from pathlib import Path
import logging
from logging import FileHandler
from datetime import datetime, date
import decimal

class FlaskEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)

class LoggingFilter(logging.Filter):
    def filter(self, record):
        if record.funcName:
            record.expandedFuncName = '%s.%s.%s:%d' % (record.name, record.module, record.funcName, record.lineno)
        else:
            record.expandedFuncName = '%s.%s:%d' % (record.name, record.module, record.lineno)
        return True

basepath = Path(__file__).parent.parent
if 'src' == basepath.name:
    basepath = basepath.parent
configpath = basepath.joinpath('resources/configuration/config.json')
with open(configpath, 'r') as f:
    config = json.load(f)
print('Configuration:', config['postgresql'])


'''
Create logging whith:
    - level = loggingconfig['level'] ()
'''
loggingconfig = config['logging']
loggingformat = '%(levelname) -7s %(asctime)-15s %(expandedFuncName)-20.20s %(message)s'
logging.basicConfig(format=loggingformat, level=loggingconfig['level'])
loggingformatter = logging.Formatter(loggingformat)
__logger = logging.getLogger()
__werkzeug__logger = logging.getLogger("werkzeug")
print(__logger)
__werkzeug__logger.addFilter(LoggingFilter())
__logger.addFilter(LoggingFilter())
configpath = basepath.joinpath('resources/traces/error.log')
if not configpath.parent.exists():
    configpath.parent.mkdir()
error_fh = FileHandler(str(configpath))
__logger.addHandler(error_fh)
error_fh.setFormatter(loggingformatter)
error_fh.setLevel(logging.ERROR)

