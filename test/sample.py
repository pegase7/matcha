from matcha.orm.data_access import DataAccess
from matcha.orm.reflection import dispatcher
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from matcha.model.Visit import Visit
from datetime import datetime
import json


if __name__ == "__main__":
    dataAccess = DataAccess()
    '''
    List des Users
    '''
    print('====================== Liste des users ======================')
    liste = dataAccess.fetch('Users')
    for element in liste:
        print(element)

    print('====================== Users 3 ======================')
    '''
    Chercher le users ayant username='Le Kiki' (unique key: un seul enregistrement
    '''
    users3 = dataAccess.find('Users', conditions=[('user_name', '=', 'Le Kiki'),])
    print(users3)
    '''
    Meme chose avec notation simplifie: Liste de condition et operateur = sont assumes
    ''' 
    users3 = dataAccess.find('Users', conditions=('user_name', 'Le Kiki'))
    print(users3)

    print('====================== Not found ======================')
    usernotfound = dataAccess.find('Users', conditions=[('user_name', '=', 'introuvable'),])
    print(usernotfound)

    if not users3 is None:    
        print('====================== Update user3 ======================')
        users3.description = 'Totalement passione des antiques femmes'
        dataAccess.merge(users3)
        print(users3)
    
    print('====================== Update user3 ======================')
    borises = dataAccess.fetch('Users', conditions=('user_name', 'borisjohnson'), joins=(['topics', 'asvisiteds', 'asvisitors', 'messages', 'connections', 'rooms']))
    if 0 < len(borises):
        for boris in borises:
            dataAccess.execute('delete from Users_topic where users_id = %s', parameters=[boris.id])
            dataAccess.execute('delete from Users_room where master_id = %s', parameters=[boris.id])
            dataAccess.execute('delete from Users_room where slave_id = %s', parameters=[boris.id])
            for visited in boris.asvisiteds:
                dataAccess.remove(visited)
            for visitor in boris.asvisitors:
                dataAccess.remove(visitor)
            for message in boris.messages:
                dataAccess.remove(message)
            for connection in boris.connections:
                dataAccess.remove(connection)
            for room in boris.rooms:
                dataAccess.remove(room)
            dataAccess.remove(boris)
        
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
    boris.popularity = 10
    dataAccess.persist(boris)
    print(boris)

    '''
    call procedure INSERT_TOPICS
        procedure requires a tuple of 2 parameters
            - users id
            - a list of unique tags 9for that pass by a set)
    '''
    tagset = set()
    for tag in ['java', 'lecture', 'sieste']:
        tagset.add(tag)
    dataAccess.call_procedure(procedure='insert_topics', parameters=(boris.id, list(tagset)))
    
    '''
    mise a jour de boris
    '''
    boris.description="Blond, intelligent mais menteur et plus menteur qu'intelligent!"
    dataAccess.merge(boris)
    print(boris)  
    
    '''
    Jointures sur 'Users_room'
    '''
    users_room = dataAccess.find('Users_room', conditions=[('master_id', 1),], joins=[('master_id', 'UM'), ('room_id')])
    if users_room:
        print(users_room.room_id, users_room.master_id, users_room.slave_id )
    
    visits = dataAccess.fetch('Visit', conditions=('visited_id', 1), joins=('visitor_id', 'V2')) #visited=1 and left join on visitor_id ==> visitor_id contains Users with id=visitor_id
    for visit in visits:
        print(visit)
        visor = visit.visitor_id
        print(' ----------------- ')
        print(type(visor))
        print(' +++++++++++++++++\n')

    visited_id = 1
    visitor_id = 2
    dataAccess = dataAccess
    visit = dataAccess.find('Visit', conditions=[('visited_id', visited_id), ('visitor_id', visitor_id)])
    if visit:
        visit.visits_number = visit.visits_number + 1
        dataAccess.merge(visit)
    else:
        visit = Visit()
        visit.visited_id = visited_id
        visit.visitor_id = visitor_id
        visit.visits_number = 1
        dataAccess.persist(visit)
        

    '''
    Serialization / Deserialization
    '''
    user1 = dataAccess.find('Users', 1)
    serial_object = json.dumps(user1, default=dispatcher.encoder_default) #Serialization
    print('Serial Object:', serial_object)
    
    deserial_object = json.loads(serial_object, object_hook=dispatcher.decoder_hook) #Deserialization
    print(deserial_object)

