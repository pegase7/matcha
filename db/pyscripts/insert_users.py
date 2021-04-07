from random import randint, shuffle
from faker import Faker
from matcha.model.Users import Users
from unidecode import unidecode
from matcha.orm.data_access import DataAccess
import logging

mail_providers = ['free.fr','gmail.com', 'hotmail.com', 'yahoo.com', 'gmx.fr', 'gmail.com', 'gmail.com', 'gmail.com', 'free.fr', 'orange.fr', 'numericable.fr']
coordinates = []

def read_towns():
    '''
    Stocke toutes les coordonnees de ville contenues dans le fichier ville.txt
    '''
    with open('../csv/ville.txt', newline='') as villetxt:
        for ville in villetxt:
            row = ville.strip().split('\t')
            coordinates.append((row[1], row[2]))
        logging.info('End populate town')

def compute_users(users, coordsize, usernames):
    provider = mail_providers[randint(0,len(mail_providers) - 1)]
    methodid = randint(0,101)
    '''
    1/100 Bi, 10/100 Homo reste Hetero
    '''
    if 100 == methodid:
        users.orientation = 'Bi'
    elif methodid < 9:
        users.orientation = 'Homo'
    else:
        users.orientation = 'Hetero'
    i = 0
    if 5 > methodid:
        users.email = str(users.first_name + '.' + users.last_name + '@' + provider).lower()
        users.user_name = str(users.first_name[0] + users.last_name).lower()
    elif 8 > methodid:
        users.email = str(users.first_name[0] + users.last_name + '@' + provider).lower()
        users.user_name = str(users.last_name + str(i)).lower()
        i += 1
    elif 8 == methodid:
        users.email = str(users.first_name[0] + '.' + users.last_name + '@' + provider).lower()
        users.user_name = str(users.last_name + users.first_name).replace(' ', '').lower()
    elif 9 == methodid:
        users.email = str(users.first_name + '_' + users.last_name + '@' + provider).lower()
        users.user_name = str(users.first_name[0] + '_' + users.last_name      ).lower()      
    else:
        users.email = str(users.last_name + str(randint(9,35)) + '@' + provider).lower()
        users.user_name = str(users.first_name[0] + '_' + users.last_name).lower()    
    users.email  = unidecode(users.email)
    users.user_name  = unidecode(users.user_name)
    '''
    Checks if duplicate username
    '''
    if users.user_name in usernames:
        i = 2
        while (users.user_name + str(i)) in usernames:
            i += 1
        users.user_name  = users.user_name + str(i)
    usernames.add(users.user_name)
    coordinate = coordinates[randint(0, coordsize - 1)]
    '''
    Les coordonnees sont les coordonnees d'une ville plus une petite modif aleatoire (evite les doublons)
    '''
    users.latitude = float(coordinate[0]) + (randint(-100,100)/10000)
    users.longitude = float(coordinate[1]) +  + (randint(-100,100)/10000)

def complete_users(users,fake, coordsize, usernames):
    users.last_name = fake.last_name()
    users.password = fake.password(special_chars=False, upper_case=False)        
    compute_users(users, coordsize, usernames)
    users.active = (randint(0,100) < 96)
    users.birthday = fake.date_between(start_date='-75y', end_date='-18y')
    users.description = None
    users.confirm = None

def populate():    
    userslist = []
    fake = Faker(['fr_FR', 'fr_CA', 'fr_QC'])
    read_towns()
    usernames = set()
    coordsize = len(coordinates)
    '''
    Creer 1000 femmes puis 1000 hommes
    '''
    for _ in range(1000):
        female = Users()
        female.gender = 'Female'
        female.first_name = fake.first_name_female()
        complete_users(female, fake, coordsize, usernames)
        userslist.append(female)
        male = Users()
        male.gender = 'Male'
        male.first_name = fake.first_name_male()
        complete_users(male, fake, coordsize, usernames)
        userslist.append(male)
    '''
    Melanger aleatoirement la liste
    '''
    shuffle(userslist)
    dataAccess = DataAccess()
    for users in userslist:
        dataAccess.persist(users, autocommit=False)
    dataAccess.commit()
    logging.info('End Users populate')
    usernames = None
