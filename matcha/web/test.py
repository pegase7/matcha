from datetime import datetime,date
import os
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from datetime import datetime

liste=[]
for i in range(1,6):
  print("/static/photo/pegase7"+str(i)+".jpg")
  if os.path.isfile("./static/photo/pegase7"+str(i)+".jpg"):
    liste.append("/static/photo/pegase7"+str(i)+".jpg")
  else:
    liste.append('/static/nophoto.jpg')
print (liste)