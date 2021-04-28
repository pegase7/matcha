import matcha.config
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
import json
import js2py

if __name__ == "__main__":
    dataAccess = DataAccess()
    populateconfig = matcha.config.config['populate']
    users1 = dataAccess.find('Users', conditions=1)
    users2 = Users()
    print(users2)
    toto = json.dumps([users1,users2], cls=matcha.config.FlaskEncoder)
    data=open('../resourcesTest/js/sjtest.js','r',encoding= 'utf8').read()
    print(type(data))
    data=js2py.eval_js(data)
    print(data('1234569'))
    