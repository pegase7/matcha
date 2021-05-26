import unittest
from matcha.model.Users import Users
from matcha.orm.data_access import DataAccess
import logging

class BorisTestCase(unittest.TestCase):

    def runTest(self):
        print("\n")
        logging.info('   +------------+')
        logging.info('   | Test Boris |')
        logging.info('   +------------+')
        data_access = DataAccess()
        borises = data_access.fetch('Users', conditions=('user_name', 'borisjohnson'), joins=(['topics', 'asvisiteds', 'asvisitors', 'messages', 'connections', 'rooms']))
        self.assertEqual(len(borises), 0, "User Boris (username='borisjohnson') already exists!")
        '''
        Create Users 'Boris'. All necessary fields must be initialized to avoid an error
        '''
        boris = Users()
        boris.first_name = 'Boris'
        boris.last_name = 'Johnson'
        boris.user_name = 'borisjohnson'
        boris.password = 'fb1691a24e1099dce33ef3d0a398b39d297f2e1c'
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
        boris.is_recommendable = True
        data_access.persist(boris)
        
        borises = data_access.fetch('Users', conditions=('user_name', 'borisjohnson'))
        self.assertEqual(len(borises), 1, "No Boris (username='borisjohnson') had been persisted!")

        tagset = set()
        self.assertIsNotNone(data_access.find('Topic','Lecture'), "tag 'lecture' does not exists")
        for tag in ['#java#', 'Lecture', '#sieste#']:
            tagset.add(tag)
        data_access.call_procedure(procedure='insert_topics', parameters=(boris.id, list(tagset)))
        self.assertIsNotNone(data_access.find('Topic','#java#'), "tag '#java#' does not exists")
        self.assertIsNotNone(data_access.find('Topic','#sieste#'), "tag '#sieste#' does not exists")
        
        result = data_access.fetch('Users_topic', ('users_id', boris.id))
        tags = []
        for topic in result:
            tags.append(topic.tag)
        self.assertEqual(len(result), 3, 'Boris must have only 3 topics!')
        tags.sort()
        self.assertEqual(tags, ['#java#', '#sieste#', 'Lecture'], "Boris must have 3 following topics: '#java#', 'Lecture', '#sieste#'!")
        
    
        '''
        mise a jour de boris
        '''
        boris.description="Blond, intelligent mais menteur et plus menteur qu'intelligent!"
        data_access.merge(boris)
    
        logging.info('Test Boris is ok')
        
        
        

if __name__ == '__main__':
    unittest.main()
