from flask import Flask, jsonify
from flask import request
from datetime import date
import json
import matcha.config
import logging
from matcha.orm.data_access import DataAccess
from decimal import Decimal


app = Flask(__name__)

@app.route('/hello/<int:postId>')
def hello_name(postId):
    return 'Hello %d!' % postId

class DecimalEncoder (json.JSONEncoder):
    def default (self, obj):
        if isinstance (obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default (self, obj)

@app.route('/hello')
def hello():
    print('ip address:', request.environ['REMOTE_ADDR'])
    jour = date.today()
    try:
        users1 = DataAccess().find('Users', conditions=1)
        print('User:',users1)
        j1 = jsonify(users1, cls = DecimalEncoder)
        j2 = j1.json
        print(j2)
        json.dumps(j2)
        print('OK')
    except (Exception) as e:
        print('KO:' + str(e))

    return 'Bonjour le monde'

if __name__ == '__main__':
#     app.add_url_rule('/avis', 'hellosdasda', hello_name)
    app.run()