#mongo GME intergrations

import pymongo
from bson.objectid import ObjectId
import pprint
import sys

client = pymongo.MongoClient("mongodb+srv://admin:tothemoon@userdata.jbuat.mongodb.net/gme?retryWrites=true&w=majority")
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Successfully connected to database")
except ConnectionFailure:
    print("Server not available")
db = client.gme
collection = db.users

#####################################################################################
#                                                                                   #
#                        SAMPLE USER PROFILE FOR REFERENCE                          #
#                       -----------------------------------                         #
#                                                                                   #
#####################################################################################
#{ 
#    'username': 'aca33334',
#    'displayname': 'AustinAlloway', 
#	 'spotify_username': 'aca0824',
#	 'sp_profile': 'Link to profile URL',
#	 'access_token': 'no clue',
#    'refresh_token': 'ctrlr',
#	 'email': 'nothings',
#	 'profile_pic': 'https://i.scdn.co/image/ab6775700000ee859bf0698648aebb835bdb6412',
#	 'age': 21,
#	 'gender': 'Male',
#	 'country': 'New Jersey',
#	 'match_pref':
#	 	{
#	        'age_min': 19,
#	        'age_max': 25,
#	        'gender': [ 'Male', 'Female']
#	    },      
#	 'favorite_users': [ ],
#	 'music_profile':
#	    {
#	    	'acousticness': 0.5,
#         	'danceability': 0.5,
#       	'energy': 0.5,
#    	    'instrumentalness': 0.5,
#   	    'liveness': 0.5,
#			'loudness': 0.5,
#			'speechiness': 0.5,
#			'tempo': 0.5,
#			'time_signature': 0.5,
#			'valence': 0.5
#	      }}

#####################################################################################
# Param: username as String, desired key name as string                             #
# Function: Return's value for given keys. Generalized getter for non-nested values.#
# RETURNS: key/value as JSON                                                        #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_keys_value(username, key):
    try:
        return collection.find_one({"username": username}, {key: 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted favorite users list                                    #
# RETURNS: List of Favorite users as JSON                                           #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_favorite_users(username):
    try:
        return collection.find_one({"username": username}, {"favorite_users": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's gender prefrences                               #
# RETURNS: gender(s) as JSON                                                        #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_match_pref_gender(username):
    try:
        return collection.find_one({"username": username}, {"match_pref": {'gender': 1}, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's max age prefrences                              #
# RETURNS: max age as JSON                                                          #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_match_pref_maxAge(username):
    try:
        return collection.find_one({"username": username}, {"match_pref": {'age_max': 1}, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's min age prefrences                              #
# RETURNS: min age as JSON                                                          #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_match_pref_minAge(username):
    try:
        return collection.find_one({"username": username}, {"match_pref": {'age_min': 1}, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's matching preferences\                           #
# RETURNS: matching preferences as JSON                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_match_pref(username):
    try:
        return collection.find_one({"username": username}, {"match_pref": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's country                                         #
# RETURNS: country as JSON                                                          #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_country(username):
    try:
        return collection.find_one({"username": username}, {"country": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's gender                                          #
# RETURNS: gender as JSON                                                           #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_gender(username):
    try:
        return collection.find_one({"username": username}, {"gender": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's age                                             #
# RETURNS: age as JSON                                                              #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_age(username):
    try:
        return collection.find_one({"username": username}, {"age": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's profile pic link                                #
# RETURNS: profile pic link as JSON                                                 #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_email(username):
    try:
        return collection.find_one({"username": username}, {"profile_pic": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's email                                           #
# RETURNS: email as JSON                                                            #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_email(username):
    try:
        return collection.find_one({"username": username}, {"email": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's spotify refresh token                           #
# RETURNS: spotify refresh token as JSON                                            #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_refresh_token(username):
    try:
        return collection.find_one({"username": username}, {"refresh_token": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's spotify access token                            #
# RETURNS: spotify access token as JSON                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_access_token(username):
    try:
        return collection.find_one({"username": username}, {"access_token": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's spotify profile link                            #
# RETURNS: spotify profile link as JSON                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_sp_profile(username):
    try:
        return collection.find_one({"username": username}, {"sp_profile": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's spotify username                                #
# RETURNS: spotify username as JSON                                                 #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_sp_username(username):
    try:
        return collection.find_one({"username": username}, {"spotify_username": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's displayname                                     #
# RETURNS: displayname as JSON                                                      #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_displayname(username):
    try:
        return collection.find_one({"username": username}, {"displayname": 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: user profile as JSON                                                       #
# Function: Adds user to database                                                   #
# RETURNS: True (inserted)                                                          #
# ON FAIL: Returns Falso (Not inserted)                                             #
#####################################################################################
def add_user(newUser):
    try:
        collection.insert_one(newUser)
        return True
    except:
        return False

#####################################################################################
# Param: ObjectID of User                                                           #
# Function: Takes user ObjectID and returns their username                          #
# RETURNS: String username                                                          #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_username(userid):
    try:
        return collection.find_one( {"_id": userid}, {"username" : 1, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String, newMusicProfile as Json                                #
# Function: Overwrites existing music profile with inputted profile                 #
# RETURNS: True                                                                     #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def update_music_profile(username, newMusicProfile):
    try:
        collection.update_many({"username": username}, { '$set' : { "music_profile": newMusicProfile}})
        return True
    except:
        return False

#####################################################################################
# Param: username as String, attribute key as string                                #
# Function: Return's denoted user's single music profile attribute value            #
# RETURNS: attribute value as json                                                  #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_music_profile_attribute(username, attribute):
    try:
        return collection.find_one({"username": username}, {"music_profile": {attribute: 1}, "_id": 0})
    except:
        return False

#####################################################################################
# Param: username as String                                                         #
# Function: Return's denoted user's entire music profile                            #
# RETURNS: music profile as JSON                                                    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_music_profile(username):
    try:
        return collection.find_one({"username": username}, {"music_profile": 1, "_id": 0})
    except:
        return False
        
# Get individual music profile attribute values

#####################################################################################
# Param: none                                                                       #
# Function: get all user profiles                                                   #
# RETURNS: user profiles                                                            #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def find_all():
    try:
        return(collection.find())
    except:
        return False

#####################################################################################
# Param: none                                                                       #
# Function: get random user profile                                                 #
# RETURNS: user profile                                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def find_one():
    try:
        return(collection.find_one())
    except:
        return False

#####################################################################################
# Param: username of User                                                           #
# Function: get user profile of denoted user                                        #
# RETURNS: user profile                                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def find_user(user):
    try:
        return(collection.find_one({ 'username': user}))
    except:
        return False

#####################################################################################
# Param: username as String, new user profile as JSON                               #
# Function: overwrite existing user profile with inputted one                       #
# RETURNS: True                                                                     #
# ON FAIL: Returns Falso                   !!!BORKED!!!                             #
#####################################################################################
def update_user(username, profile):
    try:
        collection.update_many({'username': username}, { '$set' : profile})
        return True
    except:
        return False
    

#####################################################################################
# Param: user name as String                                                        #
# Function: Checks is given username is currently in use                            #
# RETURNS: True (In use)                                                            #
# ON FAIL: Returns Falso (Not in use)                                               #
#####################################################################################
def check_username(username):
    if (collection.find_one({'username': username})):
        return True
    else:
        return False


#####################################################################################
#  This is                                                                          #
#                  Just For                                                         #
#                                   TESTING                                         #
#  Running in terminal                                    purposes                  #
#####################################################################################
## Execute certain functions based on command line arguments
## No arguments prints only successful or failed connection to database
## example terminal command: $ python3 mongo.py 1
if len(sys.argv) > 1:
    if sys.argv[1] == '1':
        for elem in find_all():
            print(elem)

    if sys.argv[1] == '2':
        print(add_user())

    if sys.argv[1] == '3':
        print(find_user(sys.argv[2]))

    if sys.argv[1] == '4':
        print(check_username(sys.argv[2]))
    
    if sys.argv[1] == '5':
        print(get_keys_value("aca33334", "match_pref"))
else:
    print("!!! No arguments given !!!")
    print("Run mongo.py with arguments 1, 2, 3, 4, etc.")
    print('example terminal command: $ python3 mongo.py 1')