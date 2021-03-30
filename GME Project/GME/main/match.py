#Match Algo
import mongo

user = mongo.find_user('k7lw')

def match_pref(user):
    prefs = user['match_pref']
    arraylist_gender_matches = genderfind(user)
    #agefind(arraylist_gender_matches)
    return arraylist_gender_matches


def genderfind(user):
    prefs = user['match_pref'][0]
    gender = prefs['gender']
    list_of_users = mongo.find_all()
    genderarray = []
    for user2 in list_of_users:
        if (user2['gender'] in gender):
            genderarray.append(user2)
    return genderarray    


def agefind(arraylist_gender_matches):
    prefs = user['match_pref']
    minage = prefs['age_min']
    maxage = prefs['age_max']
    list_of_users = arraylist_gender_matches
    for user2 in list_of_users:
        if (age_min < (user2)['age'] > age_max):
            list_of_users.remove(user2)
    return finalarray


print(match_pref(user))

#return only display name
#statement if no gender is chosen if else null