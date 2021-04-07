from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from datetime import datetime


if __name__ == "__main__":
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

    if not users3 is None:    
        print('====================== Update user3 ======================')
        users3.description = 'Totalement passione des antiques femmes'
        DataAccess().merge(users3)
        print(users3)
    
    print('====================== Update user3 ======================')
    boris = DataAccess().find('Users', conditions=('user_name', 'borisjohnson'))
    if not boris is None:
        DataAccess().remove(boris)
        
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
    Suppression de boris
    '''
    DataAccess().remove(boris)
    
    
    '''
    call procedure INSERT_TOPICS
        procedure requires a tuple of 2 parameters
            - users id
            - a list of unique tags 9for that pass by a set)
    '''
    tagset = set()
    for tag in ['java', 'lecture', 'sieste']:
        tagset.add(tag)
    DataAccess().call_procedure(procedure='insert_topics', parameters=(3, list(tagset)))
    
    users_room = DataAccess().find('Users_room', conditions=[('master_id', 1),], joins=[('master_id', 'UM'), ('room_id')])
    print(users_room.room_id, users_room.master_id, users_room.slave_id )
