from matcha.config import Config
import logging
import insert_users
import insert_topic
import insert_users_topic
import os
import traceback

def launch_sql_file(sql_file, sql_dir = '../sql/'):
    os.system('/Users/yde-mont/.brew/bin/psql -d matchadb --username matchaadmin -a -f ' + sql_dir + sql_file)

if __name__ == "__main__":
    try:
        populateconfig = Config().config['populate']
        launch_sql_file('1_drop.sql')
        launch_sql_file('2_create_ddl.sql')
        if populateconfig['test_data'] == '3_populate.sql':
                launch_sql_file('3_populate.sql')
        elif populateconfig['test_data'] == 'faker':
            insert_users.populate()
            men_topic_dict, women_topic_dict = insert_topic.populate()
            insert_users_topic.populate(men_topic_dict, women_topic_dict)     
        launch_sql_file('4_constraint.sql')
        logging.info('END POPULATE')
    except (Exception) as e:
        logging.error(str(e))
        traceback.print_exc()
        