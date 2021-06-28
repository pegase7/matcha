from matcha.config import Config
from matcha.orm.data_access import DataAccess
import logging
import insert_users
import insert_topic
import insert_users_topic
import insert_users_photo
import insert_recommend
import insert_visit
import insert_notification
import traceback
from datetime import datetime

starttime = datetime.now()


def info(message):
    endtime = datetime.now()
    logging.info(message + str(endtime) + ' - ' + str(endtime - starttime))


if __name__ == "__main__":
    try:
        populateconfig = Config(configpath='resources/configuration/configPopulate.json').config['populate']
        logging.info('Start populate' + str(starttime))
        data_access = DataAccess()
        data_access.executescript('../sql/1_drop.sql')
        data_access.executescript('../sql/2_create_ddl.sql')
        if populateconfig['test_data'] != 'faker' or populateconfig['test_data'] == 'both':
            logging.info('Populate test data')
            data_access.executescript('../sql/3_populate.sql')
            insert_users_photo.remove_current()
        if populateconfig['test_data'] == 'faker' or populateconfig['test_data'] == 'both':
            logging.info('Populate with data generated from faker:' + str(populateconfig['gender_count'] * 2) + ' users will be generated')
            insert_users.populate(populateconfig['gender_count'])
            men_topic_dict, women_topic_dict = insert_topic.populate()
            insert_users_topic.populate(men_topic_dict, women_topic_dict)
            info('Generate recommendations: ')
            insert_recommend.populate()
            info('Generate visits: ')
            insert_visit.populate()
            info('Generate notifications: ')
            insert_notification.populate()
        data_access.executescript('../sql/4_constraint.sql')
        info('END SQL - start add photos: ')
        insert_users_photo.populate(populateconfig['test_data'])
        info('END POPULATE: ')
    except (Exception) as e:
        traceback.print_exc()
        logging.error(str(e))