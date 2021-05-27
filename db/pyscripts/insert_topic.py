rom matcha.orm.data_access import DataAccess
from matcha.model.Topic import Topic
import csv
import logging

def populate():
    topics = []
    topic_dict = {}
    with open('../csv/topic.csv', newline='') as csvfile:
        topicreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in topicreader:
            topic = row[0].split(' (')[0]
            both = int(row[0].split(' (')[1].rstrip(')'))
            man = int(row[1].split(' (')[0].rstrip(')'))
            for prefix in ['le ','la ', 'les ', "l'"]:
                if topic.startswith(prefix):
                    topic = topic[len(prefix):]
            topics.append(topic)
            topic_dict[topic] = (man, both - man)
    dataAccess = DataAccess()
    for tag in topics:
        topic = Topic()
        topic.tag = tag
        dataAccess.persist(topic, autocommit=False)
    dataAccess.commit()
    logging.info('End Topic populate')
    men_total = 0
    women_total = 0
    for (men, women) in topic_dict.values():
        men_total += men
        women_total += women
    men_topic_dict = {}
    women_topic_dict = {}
    for key, value in topic_dict.items():
        men_topic_dict[key] = float(value[0]/men_total) 
        women_topic_dict[key] = float(value[1]/women_total) 
    logging.info('Step 1  Users_topic populate')
    return (men_topic_dict, women_topic_dict) 