# # import xmltodict
# # from pprint import pprint
# # import json
# # with open('temp.xml') as fd:
# #     data = json.dumps(xmltodict.parse(fd.read()))
# # print(type(data))
# # print(data["posts"]["rows"])

# # # import pymongo 
# # # mng_client = pymongo.MongoClient('localhost', 27017)
# # # mng_db = mng_client['TEST'] # Replace mongo db name
# # # collection_name = 'test' # Replace mongo db collection name
# # # db_cm = mng_db[collection_name]
 
# # # # Get the data from JSON file
# # # # with open('data.json', 'r') as data_file:
# # #     # data_json = json.load(data_file)
# # # d = {"a" : "abc","b" : "def"} 
# # # #Insert Data
# # # db_cm.remove()
# # # db_cm.insert(d)
 
# # # # Query data
# # # db_cm.UNS_Collection2.find().pretty()

import xmltodict
# import pprint
# import json

# with open('data.json', 'r') as f:
#     distros_dict = json.load(f)
import pymongo 
with open('badges.xml') as fd:
    my_dict = xmltodict.parse(fd.read())
print(type(my_dict['badges']['row']))
mng_client = pymongo.MongoClient('localhost', 27017)
mng_db = mng_client['TEST'] # Replace mongo db name
collection_name = 'test' # Replace mongo db collection name
db_cm = mng_db[collection_name]
db_cm.remove()
db_cm.insert_many(my_dict['badges']['row'])