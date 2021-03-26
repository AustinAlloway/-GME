import mongo
from mongo import *
#import sys

def menu():
    print("_____________________________________________________________________")
    print("1. Add user")
    print("2. Set username")
    print("3. Set display name")
    print("4. Get spotify username")
    print("5. Set profile picture")
    print("6. Set match preference minimum age")
    print("7. Set match preference maximum age")
    print("8. Set match preference gender")
    print("9. Get favorite users")
    print("10. Get music profile values")
    print("11. Get matches in age range")

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
    #add_user
    if sys.argv[1] == '1':
        #nombre = str(input("Enter username: "))
        pp.pprint(mongo.add_user(sys.argv[2]))
        menu()

    if sys.argv[1] == '2':
        #name = int(input("Enter username: "))
        #objid = int(input("Enter user id: "))
        pp.pprint(mongo.set_username(sys.argv[2]))
        menu()

    if sys.argv[1] == '3':
        #name = int(input("Enter username: "))
        #objid = int(input("Enter user id: "))
        pp.pprint(mongo.set_displayname(sys.argv[2]))
        menu()

    if sys.argv[1] == '4':
        pp.pprint(mongo.add_user(sys.argv[2]))
        menu()

    if sys.argv[1] == '5':
        pp.pprint(mongo.add_user(sys.argv[2]))
        menu()

    if sys.argv[1] == '6':
        pp.pprint(mongo.add_user(sys.argv[2]))
        menu()

    if sys.argv[1] == '7':
        pp.pprint(mongo.add_user(sys.argv[2]))
        menu()

    if sys.argv[1] == '3':
        pp.pprint(mongo.find_user(sys.argv[2]))
        menu()


    if sys.argv[1] == '4':
        pp.pprint(mongo.check_username(sys.argv[2]))
    

    if sys.argv[1] == '10':
        pp.pprint(mongo.get_matches_age_range(17, 19))

    #matches_age_range
    if sys.argv[1] == '11':
        low = int(input("Enter minimum age: "))
        high = int(input("Enter maximum age: "))
        for elem in mongo.get_matches_age_range(low, high):
            pp.pprint(elem)
        menu()

else:
    print("_____________________________________________________________________")
    print("!!! No arguments given !!!")
    print(menu())
    print('example terminal command: $ python3 test_data.py 1')

