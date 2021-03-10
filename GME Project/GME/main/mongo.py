#mongo GME intergrations

import pymongo
from bson.objectid import ObjectId
import pprint
import sys

print("Hello world")
client = pymongo.MongoClient("mongodb+srv://admin:tothemoon@userdata.jbuat.mongodb.net/gme?retryWrites=true&w=majority")
try:
   # The ismaster command is cheap and does not require auth.
   client.admin.command('ismaster')
   print("Successfully connected to database")
except ConnectionFailure:
   print("Server not available")
db = client.gme
collection = db.users

# Get username from ObjectID !! requires ObjectID package from bson.objectid
def get_username():
    pprint.pprint(collection.find_one( {"_id": ObjectId('6047f27a3d015cd9b40ae346')}, {"username" : 1, "_id": 0}))

# Update existing user's music profile
def update_music_profile():
    pprint.pprint(collection.update_many({"username": "aca0824"}, { '$set' : { "music_profile": {'danceability': 0.4,'energy': 0.5,'mode': 0.4,'speechiness': 0.5,'acousticness': 0.2,'instrumentalness': 0.7,'liveeness': 0.3,'valence': 0.5}}}))

# Print single user's profile from collection
def find_one():
    pprint.pprint(collection.find_one())

## Execute certian functions based on command line arguments
## No arguments just show successful or failed connection to database
## example terminal command: $ python3 testDB.py 1
if len(sys.argv) > 1:
    if sys.argv[1] == '1':
        find_one()

    if sys.argv[1] == '2':
        get_username()