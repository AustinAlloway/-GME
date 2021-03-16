from django.http import response
import requests, json, math
import numpy as np

#####################################################################################
# Param: NONE                                                                       #
# Function: Creates and checks for access Token                                     #
# RETURNS: header string used to connect to spotify API with proper auth            #
# ON FAIL: Returns Error Header String                                              #
#####################################################################################
def auth_anon():
    try:
        data = {
                'grant_type': 'client_credentials',
                'client_id': 'cad3a2d75d7e4e3681cb0479e8bfe87d',
                'client_secret': 'fba779ebdca64d09aae51d60555dc565',
            }
        auth = json.loads(requests.post("https://accounts.spotify.com/api/token", data = data).text)['access_token']
        return {"Authorization": "Bearer {}".format(auth)}
    except:
        return {"Error": "Connection Issue"}

#####################################################################################
# Param: Access Token                                                               #
# Function: Gets User info based off OAUTH Access Token                             #
# RETURNS: json response for /me api reference                                      #
# ON FAIL: Returns Error Json if Connection Issue                                   #
#####################################################################################

def get_user_info(token):
    try:
        head = {
            "Authorization": "Bearer {}".format(token)
        }
        response = requests.get("https://api.spotify.com/v1/me",headers=head).text
        return json.loads(response)
    except:
        return {"Error":"Connection Issue"}

#####################################################################################
# Param: Refresh Token and redirect URI                                             #
# Function: Gets a new acces token if the old acces token expired                   #
# RETURNS: Json of access token                                                     #
# ON FAIL: Returns Error Json if Connection Issue                                   #
#####################################################################################

def refresh_token(token,redirect_uri):
    try:
        client_id = "cad3a2d75d7e4e3681cb0479e8bfe87d"
        client_secret = "fba779ebdca64d09aae51d60555dc565"
        body_for_auth = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": "{}".format(token),
            "redirect_uri" : "{}".format(redirect_uri)
        }
        return json.loads(requests.post("https://accounts.spotify.com/api/token",data=body_for_auth).text)
    except:
        return {"Error": "Connection Issue"}

#####################################################################################
# Param: Access Code                                                                #
# Function: Tests to see if current access token is usable                          #
# RETURNS: True is token is usable                                                  #
# ON FAIL: Returns False to indicate the need to use refresh token                  #
#####################################################################################

def is_valid_token(token):
    try:
        head = {
            "Authorization": "Bearer {}".format(token)
        }
        response = requests.get("https://api.spotify.com/v1/me",headers=head).text
        if 'error' in response:
            return False
        else:
            return True
    except:
        return False


#####################################################################################
# Param: Access Code and redirect URI                                               #
# Function: Gets User Access token from access code given by part one of OAUTH flow #
# RETURNS: Json of access token                                                     #
# ON FAIL: Returns Error Json if Connection Issue                                   #
#####################################################################################

def oauth_access_token(access_code, redirect_uri):
    try:
        client_id = "cad3a2d75d7e4e3681cb0479e8bfe87d"
        client_secret = "fba779ebdca64d09aae51d60555dc565"
        body_for_auth = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": "{}".format(access_code),
            "redirect_uri" : "{}".format(redirect_uri)
        }
        return json.loads(requests.post("https://accounts.spotify.com/api/token",data=body_for_auth).text)
    except:
        return {"Error": "Connection Issue"}

#####################################################################################
# Param: Access Scopes and redirect URI                                             #
# Function: Starts oauth process with the given scopes and redirect URI             #
# RETURNS: Redirect String of the URL to log in with spotify                        #
# ON FAIL: Returns String of HOME directory                                         #
#####################################################################################

def oauth_login_redirect(scopes, redirect_uri):
    try:
        my_client_id = "cad3a2d75d7e4e3681cb0479e8bfe87d"
        return 'https://accounts.spotify.com/authorize' + '?response_type=code' + '&client_id=' + my_client_id + '&scope=' + scopes + '&redirect_uri=' + redirect_uri
    except:
        return "/"

#####################################################################################
# Param: list of genres selected by form on homepage                                #
# Function: Gets Recommended Tracks based of form selection                         #
# RETURNS: List of Track IDS for webpayer                        #
# ON FAIL: Returns String of HOME directory                                         #
#####################################################################################

def get_recommended(genres):
    request_url = "https://api.spotify.com/v1/recommendations?limit=6&seed_artists={}"
    genre_dict = {
        'country' : {
            'artist': "6roFdX1y5BYSbp60OTJWMd",
            },
        'hiphop_rb' : {
            'artist' : "3TVXtAsR1Inumwj472S9r4",
        },
        'dance' : {
            'artist': "69GGBxA162lTqCwzJG5jLp",
        },
        'alt' : {
            'artist': "7Ln80lUS6He07XvHI8qqHH",
        },
        'pop' : {
            'artist': "6vWDO969PvNqNYHIOW5v0m",
        }
    }
    #checks to see if the list of genres is empty
    if len(genres) > 0:
        artist_id_list = []
        for genre in genres:
            if(genre in genre_dict):
                #creates artist list based off selected genres
                artist_id_list.append(genre_dict[genre]['artist'])
        #creates a list of tracks based off Reccomend if can connect, returns empty list
        try:
            response_list = json.loads(requests.get(request_url.format("%2C".join(artist_id_list)),headers=auth_anon()).text)['tracks']
            tracklist = []
            for track in response_list:
                tracklist.append(track['id'])
            return tracklist
        except:
            return []
    else:
        return []


def get_music_profile_spotify(track_id_list, access_token):
    request_url = "https://api.spotify.com/v1/audio-features?ids={}"
    head = {
        "Authorization": "Bearer {}".format(access_token)
    }
    response_list = json.loads(requests.get(request_url.format("%2C".join(track_id_list)),headers=head).text)['audio_features']
    list_len = len(response_list)
    audio_features = {
            'acousticness': 0,
            'danceability': 0,
            'energy': 0,
            'instrumentalness': 0,
            'liveness': 0,
            'loudness': 0,
            'mode': 0,
            'speechiness': 0,
            'tempo': 0,
            'time_signature': 0,
            'valence': 0,
        }
    for track in response_list:
        audio_features['acousticness'] += track['acousticness']
        audio_features['danceability'] += track['danceability']
        audio_features['energy'] += track['energy']
        audio_features['instrumentalness'] += track['instrumentalness']
        audio_features['liveness'] += track['liveness']
        audio_features['loudness'] += track['loudness']
        audio_features['mode'] += track['mode']
        audio_features['speechiness'] += track['speechiness']
        audio_features['tempo'] += track['tempo']
        audio_features['time_signature'] += track['time_signature']
        audio_features['valence'] += track['valence']
        
    audio_features['acousticness'] = audio_features['acousticness']/list_len
    audio_features['danceability'] = audio_features['danceability']/list_len
    audio_features['energy'] = audio_features['energy']/list_len
    audio_features['instrumentalness'] = audio_features['instrumentalness']/list_len
    audio_features['liveness'] = audio_features['liveness']/list_len
    audio_features['loudness'] = audio_features['loudness']/list_len
    audio_features['mode'] = audio_features['mode']/list_len
    audio_features['speechiness'] = audio_features['speechiness']/list_len
    audio_features['tempo'] = audio_features['tempo']/list_len
    audio_features['time_signature'] = audio_features['time_signature']/list_len
    audio_features['valence'] = audio_features['valence']/list_len

    return audio_features

def get_top_track_list(access_token):
    head = {
        "Authorization": "Bearer {}".format(access_token)
    }
    request_url = "https://api.spotify.com/v1/me/top/tracks"
    response_list = json.loads(requests.get(request_url,headers=head).text)['items']
    top_track_id_list = []
    for track in response_list:
        top_track_id_list.append(track['id'])
    return top_track_id_list

