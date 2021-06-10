import unittest
import logging
from matcha.orm.data_access import DataAccess
from matcha.web.util1 import find_profile

class FindProfileTestCase(unittest.TestCase):
    
    def set_criteres(self, testid, userid, sexe, age_min, age_max, pop_min, pop_max, dist_max, interets, expectedresult):
        criteres={}
        criteres['id'] = userid
        users = DataAccess().find('Users', userid)
        criteres['sexe'] = sexe
        criteres['orientation'] = users.orientation if users.orientation else 'Bi'
        criteres['sexe_chercheur'] = users.gender        
        criteres['latitude'] = users.latitude
        criteres['longitude'] = users.longitude
        criteres['dist_max'] = dist_max
        if age_min:
            criteres['age_min']= age_min
        if age_max:
            criteres['age_max']= age_max
        criteres['pop_min']= pop_min
        criteres['pop_max']= pop_max
        criteres['interets'] = interets
        profile_found = find_profile(criteres)
        ids = []
        for profile in profile_found:
            ids.append(profile['id'])
        ids.sort()
        expectedresult.sort()
        self.assertEqual(ids, expectedresult, "expected values and results are different for test " + str(testid) + '!')
        return criteres

    def runTest(self):
        print("\n")
        logging.info('   +-------------------+')
        logging.info('   | Test Find Profile |')
        logging.info('   +-------------------+')
        self.set_criteres(1, 10,'Female', None, None, 0, 100, 2000, [], [13,2,24,23,18,25])
        self.set_criteres(2, 10,'Female', None, None, 0, 100, 20000, [], [13,2,11,24,23,18,25])
        self.set_criteres(3, 10,'Female', None, None, 0, 100, 200, [], [13,18])
        self.set_criteres(4, 10,'Female', None, None, 0, 100, 2000, ['Nature', 'Voyages'], [13,24])
        self.set_criteres(5, 10,'Female', None, None, 0, 100, 2000, ['Photographie', 'Cuisine', 'Television'], [13,18,23,24,25])
        self.set_criteres(6, 18,'Female', None, None, 0, 100, 2000, [], [14,17,25])
        self.set_criteres(7, 18,'Female', 25, 50, 0, 100, 2000, [], [14,25])
        self.set_criteres(8, 18,'Male', None, None, 0, 100, 2000, [], [3,9,15,5,19,7,10])
        self.set_criteres(9, 18,'Male', 25, 50, 0, 100, 2000, [], [3,9,19,15])
        self.set_criteres(10, 18,'Male', 18, 50, 0, 100, 2000, ['Cinema', 'Randonnées'], [19])
        self.set_criteres(11, 18,'Female', 18, 50, 0, 100, 2000, ['Photographie', 'Nature'], [14, 17,25])
        self.set_criteres(12, 14,'Female', None, None, 0, 100, 20000, [], [18, 17, 25])
        self.set_criteres(13, 14,'Female', None, None, 0, 100, 20000, ['Danse'], [25])
        self.set_criteres(14, 14,'Female', 18, 50, 20, 100, 20000, [], [18, 25])
        self.set_criteres(15, 19,'Female', None, None, 0, 100, 2000, [], [13,2,24,23,18,25])
        self.set_criteres(16, 19,'Female', 18, 30, 0, 100, 2000, [], [18])
        self.set_criteres(17, 19,'Female', None, None, 0, 100, 150, [], [13, 18])
        self.set_criteres(17, 16,'Male', None, None, 0, 100, 2000, [], [3, 4, 15])
        self.set_criteres(17, 16,'Male', None, None, 0, 100, 2000, ['Jeu'], [15])
        self.set_criteres(17, 15,'Male', None, None, 0, 100, 2000, [], [3, 4, 16])
        self.set_criteres(18, 15,'Male', None, None, 0, 100, 2000, ['Voyages'], [])
        self.set_criteres(19, 15,'Female', 18, 50, 0, 100, 2000, [], [23, 18,25])
        self.set_criteres(20, 15,'Female', None, None, 0, 100, 2000, ['Gastronomie'], [18,23,24,25])
        self.set_criteres(21, 15,'Female', 30, 50, 0, 100, 20000, [], [6,11,23,25])
        self.set_criteres(22, 23,'Male', None, None, 0, 100, 2000, [], [3,9,5,7,10,15,19])
        self.set_criteres(23, 23,'Male', 40, 50, 0, 100, 2000, [], [3])
        self.set_criteres(24, 23,'Male', None, None, 0, 100, 2000, ['Peinture', 'Musée', 'Informatique'], [5, 7, 10])
        self.set_criteres(25, 23,'Male', 50, 75, 0, 100, 2000, [], [5, 10])
        
if __name__ == '__main__':
    unittest.main()