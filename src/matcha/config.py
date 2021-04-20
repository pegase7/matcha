import json
from pathlib import Path
import logging
from logging import FileHandler
from datetime import datetime, date
import decimal
from matcha.orm.reflection import ModelObject

'''
Encoder used when deserializing for communicqtion with JavaScript 
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
__logger = logging.getLogger()
__werkzeug__logger = logging.getLogger("werkzeug")
loggingformat = '%(levelname) -7s %(asctime)-15s%(lineno)4s:%(module lineno)-20.20s: %(message)s'
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG
)

configpath = basepath.joinpath('resources/traces/error.log')
if not configpath.parent.exists():
    configpath.parent.mkdir()
error_fh = FileHandler(str(configpath))
__logger.addHandler(error_fh)
error_fh.setFormatter(logging.Formatter(loggingformat))
error_fh.setLevel(logging.ERROR)

