from datetime import datetime,date
import os
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from datetime import datetime


a ={
  "ip":"46.231.218.157",
  "type":"ipv4",
  "continent_code":"EU",
  "continent_name":"Europe",
  "country_code":"FR",
  "country_name":"France",
  "region_code":"IDF",
  "region_name":"\u00cele-de-France",
  "city":"Saint-Ouen",
  "zip":"75001",
  "latitude":48.8602294921875,
  "longitude":2.3410699367523193,
  "location":{
    "geoname_id":2977824,
    "capital":"Paris",
    "languages":[
      {
        "code":"fr",
        "name":"French",
        "native":"Fran\u00e7ais"
      }
    ],
    "country_flag":"http:\/\/assets.ipstack.com\/flags\/fr.svg",
    "country_flag_emoji":"\ud83c\uddeb\ud83c\uddf7",
    "country_flag_emoji_unicode":"U+1F1EB U+1F1F7",
    "calling_code":"33",
    "is_eu":True
  }
}
print (a['latitude'], a['longitude'])
    