import os
import tkinter as tk

from datetime import datetime
from matcha.orm.data_access import DataAccess

dateconnection=datetime.now()

print(dateconnection)
#tags = DataAccess().find('Users_topic', conditions=('users_id',5))
#print(tags[0])
tops = DataAccess().fetch('Users_topic', conditions=('users_id',5))
tags=[]
for t in tops:
        tags.append(t.tag)
print (tags)
#os.remove('matcha/web/static/photo/pegase73.jpg')
#fichier = open("pegase.txt", "w")
#fichier.close