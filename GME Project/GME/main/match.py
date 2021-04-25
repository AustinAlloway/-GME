#Match Algo
import mongo
import pprint as pp

def match_pref(username_in_session):
    user = mongo.find_user(username_in_session)
    arraylist_gender_matches = genderfind(user)
    agematch = agefind(arraylist_gender_matches, user)
    return musicpref(agematch, user)


def genderfind(user):
    prefs = user['match_pref']
    gender = prefs['gender']
    list_of_users = mongo.find_all()
    genderarray = []
    for user2 in list_of_users:
        if (user2['gender'] in gender):
            genderarray.append(user2)
    return genderarray


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

def matchability(user, user3):
    music_pref = user['music_profile'][0]
    #usermatchability = (music_pref['danceability']+music_pref['energy']+music_pref['valence'])/3
    user4match = user3['music_profile'][0]
    #user4matchability = (user4match['danceability']+user4match['energy']+user4match['valence'])/3
    #matchability = (user4matchability/usermatchability)*100
    usermatcha = ((music_pref['danceability']+music_pref['energy']+music_pref['valence'])*100)/3 
    usermatcha2 = ((user4match['danceability']+user4match['energy']+user4match['valence'])*100)/3
    matchaDiff = (100 - abs(((usermatcha - usermatcha2)/((usermatcha + usermatcha2)/2) * 100)))
    print(matchaDiff)
    return matchaDiff

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
                    user3['matchability']=matchpercent
                    #mongo.set_keys_value(user3, 'matchability', matchpercent)
                    finalMatches.append(user3)


    return finalMatches
    #return sort_matches(finalMatches)

#def sort_matches(matchList):
 #   sortedList = sorted(matchList, reverse=True, key = lambda match: match['matchability'])
  #  return sortedList

match_pref('k7lw')
'''
test_username = "k7lw"
for user in match_pref(test_username):
    print(user['displayname'])
    print(user['profile_pic'])
    print(user['age'])
    print(user['gender'])
    print(user['country'])
    print(user['matchability'])
'''