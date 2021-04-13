#mongo GME intergrations

import pymongo
from bson.objectid import ObjectId
import pprint as pp
import json
import sys
from numpy import random
import re

client = pymongo.MongoClient("mongodb+srv://admin:tothemoon@userdata.jbuat.mongodb.net/gme?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
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
#    'username': 'aca0824',
#    'displayname': 'AustinAlloway', 
#	 'spotify_username': 'aca0824',
#	 'sp_profile': 'https://open.spotify.com/user/aca0824',
#	 'access_token': 'NgCXRK...MzYjw',
#    'refresh_token': 'NgAagA...Um_SHo',
#	 'email': 'email@example.com',
#	 'profile_pic': 'https://i.scdn.co/image/ab6775700000ee859bf0698648aebb835bdb6412',
#	 'age': 21,
#	 'gender': 'Male',
#	 'country': 'United States',
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
#	     }
# }

# ---------------------------
# Functions Expected per Page
# ---------------------------
#
# Home Page:
#   - add_user()
#
# Profile Page:
#   - set_username()
#   - set_displayname()
#   - get_sp_username()
#   - set_profile_pic()
#   - set_match_pref_minAge()
#   - set_match_pref_maxAge()
#   - set_match_pref_gender()
#   - get_favorite_users()
#   - get_music_profile()
#
# Match Making Page:
#   - get_matches_age_range()



#
#   Getter Functions
#

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
# Param: username of User                                                           #
# Function: get user profile of denoted user                                        #
# RETURNS: user profile                                                             #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def user_exist(user):
    try:
        for user_data in find_all():
            if(user == user_data['username']):
                return True
        return False
    except:
        return False

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
def get_profile_pic(username):
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

#
#   Setter Functions
#

#####################################################################################
# Param: username as String, desired key name as string, value as JSON              #
# Function: update user's profile key value by denoted key and value                #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_keys_value(username, key, value):
    try:
        collection.update_one({"username": username}, { '$set' : {key: value}})
    except:
        return False

#####################################################################################
# Param: username as String, List of favorited Users as JSON                        #
# Function: Updates user's entire favorited users list                              #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_favorite_users(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "favorite_users": value}})
    except:
        return False

#####################################################################################
# Param: username as String, gender as JSON array                                   #
# Function: updates user's gender preference                                        #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_match_pref_gender(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "match_pref.gender": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Max age as int                                         #
# Function: set's user match pref.'s max age                                        #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_match_pref_maxAge(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "match_pref.age_max": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Min age as int                                         #
# Function: set's user match pref.'s min age                                        #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_match_pref_minAge(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "match_pref.age_min": value}})
    except:
        return False

#####################################################################################
# Param: username as String, match preferences as JSON                              #
# Function: Updates user's entire match preferences                                 #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_match_pref(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "match_pref": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Country as String                                      #
# Function: Updates user's country                                                  #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_country(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "country": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Gender as String                                       #
# Function: Sets user's gender                                                      #
# RETURNS: No Return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_gender(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "gender": value}})
    except:
        return False

#####################################################################################
# Param: username as String, age as int                                             #
# Function: sets user's age                                                         #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_age(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "age": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Link to picture as String                              #
# Function: Updates user's profile picture                                          #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_profile_pic(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "profile_pic": value}})
    except:
        return False

#####################################################################################
# Param: username as String, email as String                                        #
# Function: updates user's email                                                    #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_email(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "email": value}})
    except:
        return False

#####################################################################################
# Param: username as String, refresh token as string                                #
# Function: sets user's sporitfy refresh token                                      #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_refresh_token(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "refresh_token": value}})
    except:
        return False

#####################################################################################
# Param: username as String, access token as string                                 #
# Function: sets user's spotify access token                                        #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_access_token(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "access_token": value}})
    except:
        return False

#####################################################################################
# Param: username as String, profile link as string                                 #
# Function: Set user's spotify profile link                                         #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_sp_profile(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "sp_profile": value}})
    except:
        return False

#####################################################################################
# Param: username as String, spotify username as string                             #
# Function: set user's spotify username                                             #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_sp_username(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "spotify_username": value}})
    except:
        return False

#####################################################################################
# Param: username as String, Display name as string                                 #
# Function: set user's displayname                                                  #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_displayname(username, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "displayname": value}})
    except:
        return False

#####################################################################################
# Param: ObjectID of User, username as string                                       #
# Function: sets user's GME username                                                #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_username(username, value):
    try:
        collection.update_one( {"username": username}, { '$set' : { "username": value}})
    except:
        return False

        
#####################################################################################
# Param: username as String, attribute key as string, value as float                #
# Function: Update denoted user's single music profile attribute value              #
# RETURNS: No return                                                  #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def set_music_profile_attribute(username, attribute, value):
    try:
        collection.update_one({"username": username}, { '$set' : { "music_profile": {attribute: value}}})
    except:
        return False

#
#   Generaly Misc. Functions
#

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
# Param: user as String (username), favUser as String (username)                    #
# Function: adds favUser to user's favorite_user list                               #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def add_favorited_user(user, favUser):
    try: 
        collection.update_many({"username": user}, { "$addToSet": {"favorite_users": favUser}})
    except:
        return False

#####################################################################################
# Param: user as String (username), favUser as String (username)                    #
# Function: removes favUser from user's favorite_user list                          #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def remove_favorited_user(user, favUser):
    try: 
        collection.update_many({"username": user}, { "$pull": {"favorite_users": favUser}})
    except:
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: randomize all user's gender preferences to random genders (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_profile_pics():
    try:
        k = 1
        for elem in find_all():
            collection.update_one({'username': elem['username']}, { '$set' : { 'profile_pic': 'https://picsum.photos/id/' + str(k) + '/200'}})
            print("yes")
            k += 1
    except:
        print("no")
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: randomize all user's gender preferences to random genders (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_match_pref_empty():
    try:
        for elem in find_all():
            k = random.randint(18, 26)
            collection.update_one({'username': elem['username']}, { '$set' : { "match_pref": {}}})
    except:
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: randomize all user's gender preferences to random genders (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_match_pref_genders():
    try:
        for elem in find_all():
            k = random.randint(1, 3) 
            genders = json.loads(json.dumps(random.choice(['Male', 'Female', 'Non'], k).tolist()))
            collection.update_one({'username': 'k7lw'}, { '$set' : { "match_pref.gender": genders}})
    except:
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: randomize all user's gender preferences to random genders (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_match_pref_maxAge():
    try:
        for elem in find_all():
            k = random.randint(26, 49)
            collection.update_one({'username': elem['username']}, { '$set' : { "match_pref.age_max": k}})
    except:
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: randomize all user's gender preferences to random genders (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_match_pref_minAge():
    try:
        for elem in find_all():
            k = random.randint(18, 26)
            collection.update_one({'username': elem['username']}, { '$set' : { "match_pref.age_min": k}})
    except:
        return False

#####################################################################################
# Param: N/A                                                                        #
# Function: Randomize all user's favorited user's list             (USE ONLY WITH   #
# RETURNS: No return                                                SAMPLE DATA)    #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
#
# CURRENT ISSUE: Sample from random.choice is repeatable. Could see gender preference of ['Non', 'Non'] etc.
def randomize_all_favorite_users():
    all_users = []
    try:
        for elem in find_all():
            all_users.append(elem['username'])
        for elem in find_all():
            k = random.randint(1, 9) 
            fav_users = json.loads(json.dumps(random.choice(all_users, k).tolist()))
            collection.update_one({'username': elem['username']}, { '$set' : { "favorite_users": fav_users}})
    except:
        print("false")
        return False

#####################################################################################
# Param: minAge as int, maxAge as int                                               #
# Function: Returns username and age of all users within age range                  #
# RETURNS: No return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def get_matches_age_range(minAge, maxAge):
    try:
        return collection.find({"age": {"$gte": minAge, "$lte": maxAge}}, {"username": 1, "age":1, "_id":0})
    except:
        return False

#####################################################################################
# Param: none                                                                       #
# Function: set music attributes closer to matchmaking algorithms as necessary      #
# RETURNS: no return                                                                #
# ON FAIL: Returns Falso                                                            #
#####################################################################################
def musicAttributeEditor():
    try:
        authorized_users = ['k7lw','nitbaba','arcanebelal','newburyrn','12151060767','af8jd8mix7th4gk3cp6xqqo5a']
        for elem in find_all():
            if(not (elem['username'] in authorized_users)):
                valenceVal = random.uniform(0.273050, 0.637117)
                energyVal = random.uniform(0.370575, 0.864676)
                danceabilityVal = random.uniform(0.349833, 0.816276)
                elem['music_profile'][0]['valence'] = valenceVal
                elem['music_profile'][0]['energy'] = energyVal
                elem['music_profile'][0]['danceability'] = danceabilityVal
                update_music_profile(elem['username'], elem['music_profile'])
    except:
        return False


#####################################################################################
# Param: Profile creation info                                                      #
# Function: formats a user for database entry                                       #
# RETURNS: Profile format                                                           #
#####################################################################################
def profile_formatter(username,display_name,spotify_username,sp_profile,access_token,refresh_token,email,
profile_pic,age,gender,country,match_pref,favorite_users,music_profile):

    return {
        'username': username,
        'displayname': display_name, 
        'spotify_username': spotify_username,
        'sp_profile': sp_profile,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'email': email,
        'profile_pic': profile_pic,
        'age': age,
        'gender': gender,
        'country': country,
        'match_pref': match_pref,      
        'favorite_users': favorite_users,
        'music_profile': music_profile
        }

#####################################################################################
# Param: N/A                                                                        #
# Function: adds mock data into database                                            #
# RETURNS: Confirmation message                                                     #
#####################################################################################
def data_add():
    with open('../static/GME_MOCK_DATA.json') as mock:
        data = json.load(mock)

        for i in data:
            if(user_exist(i['username']) == False):
                add_user(i)
            else:
                print("User exist")
    
    mock.close()


def fix_data():
    for user in find_all():
        try:
            user['music_profile'][0]
            print('array exists')
        except:
            dummy_mp = [user['music_profile']]
            update_music_profile(user['username'],dummy_mp)  
            print('fixed' + user['username']) 

