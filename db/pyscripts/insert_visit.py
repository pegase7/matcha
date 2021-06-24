from matcha.orm.data_access import DataAccess
from random import randint
from datetime import datetime, timedelta
from matcha.orm.reflection import ModelDict
from matcha.model.Visit import Visit

DATA_ACCESS = None


def populate():
    global DATA_ACCESS
    DATA_ACCESS = DataAccess()
    '''
        mean = 107, min =60, max = 200
        delta seconds = 1571680000
    '''

    # Change 'created' and 'last_update' fields so that they are no longer computed and can be set in this module 
    visitmodel = ModelDict().get_model_class('Visit')
    visitmodel.get_field('created').iscomputed = False
    visitmodel.get_field('last_update').iscomputed = False   
    
    recommends = DATA_ACCESS.fetch('Users_recommendation', joins=['sender_id', 'receiver_id'])
    
    nb = 0
    today = datetime.now()
    for recommend in recommends:
        has_visit = ((recommend.weighting - 60) / 140 * randint(0, 100)) > 25
        if has_visit:
            visit = Visit()
            date_sup = recommend.sender_id.created if recommend.sender_id.created > recommend.receiver_id.created else recommend.receiver_id.created
            days_between = (today - date_sup).days
            visit.visited_id = recommend.receiver_id.id
            visit.visitor_id = recommend.sender_id.id
            delta = randint(0, days_between) - 5
            visit.created = date_sup + timedelta(days=delta, milliseconds=randint(0, 86400000))
            visit.visits_number = randint(1, 4)
            visit.last_update = visit.created if visit.visits_number == 1 else date_sup + timedelta(days=randint(delta, days_between), milliseconds=randint(0, 86400000))
            visit.isfake = (randint(1, 80) == 1)
            visit.isblocked = (visit.isfake == False) and (randint(1, 25) == 1) 
            visit.islike = (visit.isfake == False) and (visit.isblocked == False) and (randint(1, 4) != 1) 
            DATA_ACCESS.persist(visit, autocommit=False) 
            nb = nb + 1
    DATA_ACCESS.commit()

                 
if '__main__' == __name__:
    populate()
