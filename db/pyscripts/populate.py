from matcha.config import Config
from matcha.orm.data_access import DataAccess
import logging
import insert_users
import insert_topic
import insert_users_topic
import traceback

if __name__ == "__main__":
    try:
        populateconfig = Config(configpath='resources/configuration/configPopulate.json').config['populate']
        data_access = DataAccess()
        data_access.executescript('../sql/1_drop.sql')
        data_access.executescript('../sql/2_create_ddl.sql')
        if populateconfig['test_data'] != 'faker' or populateconfig['test_data'] == 'both':
            data_access.executescript('../sql/3_populate.sql')
        if populateconfig['test_data'] == 'faker' or populateconfig['test_data'] == 'both':
            insert_users.populate()
            men_topic_dict, women_topic_dict = insert_topic.populate()
            insert_users_topic.populate(men_topic_dict, women_topic_dict)
        data_access.executescript('../sql/4_constraint.sql')
        logging.info('END POPULATE')
    except (Exception) as e:
        traceback.print_exc()
        logging.error(str(e))
