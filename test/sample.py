from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from datetime import datetime
import logging
from pickle import NONE


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    '''
    List des Users
    '''
    print('====================== Liste des users ======================')
    liste = DataAccess().fetch('Users')
    for element in liste:
        print(element)

    print('====================== Users 3 ======================')
    '''
    Chercher le users ayant username='Le Kiki' (unique key: un seul enregistrement
    '''
    users3 = DataAccess().find('Users', conditions=[('user_name', '=', 'Le Kiki'),])
    print(users3)
    '''
    Meme chose avec notation simplifie: Liste de condition et operateur = sont assumes
    ''' 
    users3 = DataAccess().find('Users', conditions=('user_name', 'Le Kiki'))
    print(users3)

    print('====================== Not found ======================')
    usernotfound = DataAccess().find('Users', conditions=[('user_name', '=', 'introuvable'),])
    print(usernotfound)
    
    print('====================== Update user3 ======================')
    users3.description = 'Totalement passione des antiques femmes'
    DataAccess().merge(users3)
    print(users3)
    
    print('====================== Update user3 ======================')
    '''
    Creation du Users Boris. Tous les champs necessaire doivent etre initialise pour eviter une erreur
    '''
    boris = Users()
    boris.first_name = 'Boris'
    boris.last_name = 'Johnson'
    boris.user_name = 'borisjohnson'
    boris.password = 'ElisabethGetOnMyNerves'
    boris.description = 'Blond, intelligent mais menteur'
    boris.email = 'boris.johnson@england.uk'
    boris.active = True
    boris.confirm = None
    boris.gender = 'Male'
    boris.orientation = 'Hetero'
    boris.birthday = '1964-06-19'
    boris.latitude = None
    boris.longitude = None
    DataAccess().persist(boris)
    print(boris)

    '''
    mise a jour de boris
    '''
    boris.description="Blond, intelligent mais menteur et plus menteur qu'intelligent!"
    DataAccess().merge(boris)
    print(boris)
    
    '''
    Suppression de Borid
    '''
    DataAccess().remove(boris)
    
