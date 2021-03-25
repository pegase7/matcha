import json
from pathlib import Path

basepath = Path(__file__).parent.parent
if 'src' == basepath.name:
    basepath = basepath.parent
basepath = basepath.joinpath('resources/configuration/config.json')
with open(basepath, 'r') as f:
    config = json.load(f)
print('Configuration:', config['postgresql'])