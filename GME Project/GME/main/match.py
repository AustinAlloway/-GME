#Match Algo
import mongo

def match_pref(username_in_session):
    user = mongo.find_user(username_in_session)
    arraylist_gender_matches = genderfind(user)
    return agefind(arraylist_gender_matches, user)


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

test_username = "k7lw"

for user in match_pref(test_username):
    print(user['displayname'])
    print(user['profile_pic'])
    print(user['age'])
    print(user['gender'])
    print(user['country'] + "\n")
    #% of matchability
