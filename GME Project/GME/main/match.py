#Match Algo
from . import mongo

def match_pref(username_in_session):
    user = mongo.find_user(username_in_session)
    arraylist_gender_matches = genderfind(user)
    agematch = agefind(arraylist_gender_matches, user)
    return musicpref(agematch,user)


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


def musicpref(agematch, user):
    music_pref = user['music_profile'][0]
    finalMatches = []
    for user3 in agematch:
        musicpref_of_user3 = user3['music_profile'][0]
        if (float(music_pref['danceability']) < float(musicpref_of_user3['danceability']) * 1.3
        and float(music_pref['danceability']) > float(musicpref_of_user3['danceability']) * 0.7):
            #print('dance')
            if (float(music_pref['energy']) < float(musicpref_of_user3['energy']) * 1.3
            and float(music_pref['energy']) > float(musicpref_of_user3['energy']) * 0.7):
                #print('energy')
                if (float(music_pref['valence']) < float(musicpref_of_user3['valence']) * 1.3
                and float(music_pref['valence']) > float(musicpref_of_user3['valence']) * 0.7):
                    #print('valence')
                    finalMatches.append(user3)

                ##if (float(music_pref['loudness']) < float(musicpref_of_user3['loudness']) * 1.3
                ##and float(music_pref['loudness']) > float(musicpref_of_user3['loudness']) * 0.7):
                ##    print(3)

    return finalMatches

test_username = "k7lw"
'''
for user in match_pref(test_username):
    print(user['displayname'])
    print(user['profile_pic'])
    print(user['age'])
    print(user['gender'])
    print(user['country'] + "\n")
    #% of matchability
    '''
