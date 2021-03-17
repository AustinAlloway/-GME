import mongo


user1 = {
    "username": "msterrie0",
    "displayname": "Morgan Sterrie",
    "spotify_username": "msterrie0",
    "email": "msterrie0@imdb.com",
    "profile_pic": "http://dummyimage.com/214x128.png/ff4444/ffffff",
    "age": 32,
    "gender": "Neither",
    "country": "Macedonia",
    "match_pref": [
      {
        "age_min": 25,
        "age_max": 67,
        "gender": [
  
        ]
      }
    ],
    "favorite_users": [
  
    ],
    "music_profile": [
      {
        "acousticness": 0.25,
        "danceability": 0.47,
        "energy": 0.02,
        "instrumentalness": 0.96,
        "liveness": 0.46,
        "loudness": 0.4,
        "speechiness": 0.34,
        "tempo": 0.36,
        "time_signature": 0.74,
        "valence": 0.36
      }
    ]
}

mongo.add_user(user1)