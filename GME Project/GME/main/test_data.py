import mongo
from mongo import *

def menu():
    print("_____________________________________________________________________")
    print("1. Get matches in age range")
    print("2. Get music profile values")
    print("3. Get favorite users")
    print("4. Get match preferences")
    print("5. Check user exist")
    print("6. Find user")   

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
    #matches_age_range
    if sys.argv[1] == '1':
        for elem in mongo.get_matches_age_range(int(input("Enter minimum age: ")), int(input("Enter maximum age: "))):
            pp.pprint(elem)
        menu()

    #music_profile_values
    if sys.argv[1] == '2':
        pp.pprint(mongo.get_music_profile(input("Enter username: ")))
        menu()
    
    #favorite users
    if sys.argv[1] == '3':
        pp.pprint(mongo.get_favorite_users(input("Enter username: ")))
        menu()

    #favorite users
    if sys.argv[1] == '4':
        pp.pprint(mongo.get_match_pref(input("Enter username: ")))
        menu()

    #user_exist
    if sys.argv[1] == '5':
        exists = mongo.check_username(input("Enter username: "))
        if(exists == True):
            print("Username in use :(")
        else:
            print("Username not in use :)")
        menu()

    #find_user
    if sys.argv[1] == '6':
        pp.pprint(mongo.find_user(input("Enter username: ")))
        menu()

        #favorite users
    if sys.argv[1] == '7':
        pp.pprint(mongo.randomize_all_profile_pics())
        menu()
else:
    print("_____________________________________________________________________")
    print("!!! No arguments given !!!")
    print(menu())
    print('example terminal command: $ python3 test_data.py 1')

