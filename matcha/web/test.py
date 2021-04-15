from datetime import datetime,date
import os
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users


liste = DataAccess().fetch('Users')
print(type(46.10904))
for user in liste:
    if user.birthday:
  
        #print('age :', datetime.now()-user.birthday)
        today = date.today()
        try: 
            birthday = user.birthday.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = user.birthday.replace(year=today.year, month=user.birthday.month+1, day=1)
        if birthday > today:
            print( today.year - user.birthday.year - 1)
        else:
            print(today.year - user.birthday.year)

