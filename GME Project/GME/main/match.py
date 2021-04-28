#Match Algo
from . import mongo
import pprint as pp

#####################################################################################
# Param: username of session user                                                   #
# Function: Creates List of matched users based of speicified match prefereences    #
# RETURNS: List of matched users based of speicified match prefereences             #
#####################################################################################

def match_pref(username_in_session):
    user = mongo.find_user(username_in_session)
    arraylist_gender_matches = genderfind(user)
    agematch = agefind(arraylist_gender_matches, user)
    return musicpref(agematch, user)


#####################################################################################
# Param: session user obejct                                                        #
# Function: Creates List of matched users based of speicified genders               #
# RETURNS: List of matched users based of speicified gender                         #
#####################################################################################

def genderfind(user):
    prefs = user['match_pref']
    gender = prefs['gender']
    list_of_users = mongo.find_all()
    genderarray = []
    for user2 in list_of_users:
        if (user2['gender'] in gender):
            genderarray.append(user2)
    return genderarray


#####################################################################################
# Param: match gender list and user of session                                      #
# Function: Creates List of matched users based of speicified age                   #
# RETURNS: List of matched users based of speicified age                            #
#####################################################################################

def agefind(arraylist_gender_matches, user):
    prefs = user['match_pref']
    minage = prefs['age_min']
    maxage = prefs['age_max']
    list_of_users = arraylist_gender_matches
    successfulmatchlist = [] 
    for user2 in list_of_users:
        if (minage < (user2)['age'] and (user2)['age'] < maxage):
            successfulmatchlist.append(user2)
    return successfulmatchlist


#####################################################################################
# Param: user object of session user, and user object fo comparer obj               #
# Function: creates numeric value of match percentage                               #
# RETURNS: match percentage                                                         #
#####################################################################################

def matchability(user, user3):
    music_pref = user['music_profile'][0]
    user4match = user3['music_profile'][0]
    usermatcha = ((music_pref['danceability']+music_pref['energy']+music_pref['valence'])*100)/3 
    usermatcha2 = ((user4match['danceability']+user4match['energy']+user4match['valence'])*100)/3
    matchaDiff = (100 - abs(((usermatcha - usermatcha2)/((usermatcha + usermatcha2)/2) * 100)))
    return matchaDiff



#####################################################################################
# Param: list of matches                                                            #
# Function: sort the list of amtches into highest matchability first                #
# RETURNS: List of matched users sorted by highest match first                      #
#####################################################################################

def sort_matches(matchList):
    sortedList = sorted(matchList, reverse=True, key = lambda match: match['matchability'])
    return sortedList


#####################################################################################
# Param: user match list and session user object                                    #
# Function: Creates a list of matches based off music preferences                   #
# RETURNS: The final list of matches based off music preferences that is sorted     #
#####################################################################################


def musicpref(agematch, user):
    music_pref = user['music_profile'][0]
    finalMatches = []
    for user3 in agematch:
        musicpref_of_user3 = user3['music_profile'][0]
        if (float(music_pref['danceability']) < float(musicpref_of_user3['danceability']) * 1.3
        and float(music_pref['danceability']) > float(musicpref_of_user3['danceability']) * 0.7):

            if (float(music_pref['energy']) < float(musicpref_of_user3['energy']) * 1.3
            and float(music_pref['energy']) > float(musicpref_of_user3['energy']) * 0.7):

                if (float(music_pref['valence']) < float(musicpref_of_user3['valence']) * 1.3
                and float(music_pref['valence']) > float(musicpref_of_user3['valence']) * 0.7):

                    matchpercent = matchability(user, user3)
                    user3['matchability']= str(matchpercent)[0:5]
                    finalMatches.append(user3)

    return sort_matches(finalMatches)
