from random import randint, shuffle
from faker import Faker
from unidecode import unidecode
from matcha.model.Users import Users
from matcha.orm.data_access import DataAccess

mail_providers = ['free.fr','gmail.com', 'hotmail.com', 'yahoo.com', 'gmx.fr', 'gmail.com', 'gmail.com', 'gmail.com', 'free.fr', 'orange.fr', 'numericable.fr']
coordinates =[]
coordsize = 0

def read_towns():
    '''
    Stocke toutes les coordonnees de ville contenues dans le fichier ville.txt
    '''
    with open('../resourcesTest/csv/ville.txt', newline='') as villetxt:
        for ville in villetxt:
            row = ville.strip().split('\t')
            coordinates.append((row[1], row[2]))

def compute_users(users):
    provider = mail_providers[randint(0,len(mail_providers) - 1)]
    methodid = randint(0,11)
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
    coordinate = coordinates[randint(0,coordsize - 1)]
    '''
    Les coordonnees sont les coordonnees d'une ville plus une petite modif aleatoire (evite les doublons)
    '''
    users.latitude = float(coordinate[0]) + (randint(-100,100)/10000)
    users.longitude = float(coordinate[1]) +  + (randint(-100,100)/10000)

def complete_users(users,fake):
#    users.id = 1
    users.last_name = fake.last_name()
    users.password = fake.password(special_chars=False, upper_case=False)        
    compute_users(users)
    users.active = (randint(0,100) < 96)
    users.birthday = fake.date_between(start_date='-75y', end_date='-18y')
    users.description = None
    users.confirm = None
    
if __name__ == "__main__":
    userslist = []
    fake = Faker(['fr_FR', 'fr_CA', 'fr_QC'])
    read_towns()
    coordsize = len(coordinates)
    print('---------------------')
    '''
    Creer 1000 femmes puis 1000 hommes
    '''
    for _ in range(1000):
        female = Users()
        female.gender = 'Female'
        female.first_name = fake.first_name_female()
        complete_users(female, fake)
        userslist.append(female)
        male = Users()
        male.gender = 'Male'
        male.first_name = fake.first_name_male()
        complete_users(male, fake)
        userslist.append(male)
    shuffle(userslist)
    for users in userslist:
        DataAccess().persist(users)
