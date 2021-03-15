import mongo as m

for x in m.find_all():
    print(x)
print("\n\n\n")
print(m.find_user('aca33334'))