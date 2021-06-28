from matcha.orm.data_access import DataAccess
import numpy as np
import logging
from shutil import copyfile
import os

photo_dir = '../../src/matcha/web/static/photo/'
photo_oli = '../../resourcesTest/photo_oli/'


def remove_current():
    for f in os.listdir(photo_dir):
        os.remove(photo_dir + f)


def populatetest():
    for f in os.listdir(photo_oli):
        copyfile(photo_oli + f, photo_dir + f)


def populatefaker():
    dataAccess = DataAccess()
    userslist = dataAccess.fetch('Users')
    keys = range(1, 346)
    for users in userslist:
        nbphotos = np.random.randint(1, 5)
        photos = np.random.choice(keys, nbphotos, replace=False)
        i = 1
        for photo in photos:
            copyfile('../../resourcesTest/Cranes/' + str(photo) + '.jpg', photo_dir + users.user_name + str(i) + '.jpg')
            i += 1


def populate(populateconfig):
    remove_current()
    if populateconfig != 'faker' or populateconfig == 'both':
        populatetest()
    if populateconfig == 'faker' or populateconfig == 'both':
        populatefaker()


if __name__ == "__main__":
    # populate()
    remove_current()
    populatetest()