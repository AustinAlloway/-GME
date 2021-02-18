import requests, json, math
import numpy as np
data = {
        'grant_type': 'client_credentials',
        'client_id': 'cad3a2d75d7e4e3681cb0479e8bfe87d',
        'client_secret': '723862ec272a4f7393d02bebae510fd2',
    }
auth = json.loads(requests.post("https://accounts.spotify.com/api/token", data = data).text)['access_token']
header = {
    "Authorization": "Bearer {}".format(auth)
}

def get_genre_from_artist_list(inputArtistList):
    if (len(inputArtistList) > 0):
        output_genre_list = []
        numb_requests = math.ceil(len(inputArtistList) / 50)
        splitted = np.array_split(inputArtistList ,numb_requests)
        for list in splitted:
            artist_string = ','.join(list)
            response = json.loads(requests.get('https://api.spotify.com/v1/artists?ids={}'.format(artist_string),headers = header).text)['artists']
            for artist in response:
                output_genre_list = output_genre_list + artist['genres']
        return output_genre_list
    else:
        return[]

def get_artist_list_from_playlist(playlist_id):
    list_of_tracks = json.loads(requests.get('https://api.spotify.com/v1/playlists/{}'.format(playlist_id),headers=header).text)['tracks']['items']
    list_of_artists = []
    for track in list_of_tracks:
        if (track['track']['artists'][0]['id'] is None):
            pass
        else:
            list_of_artists.append(track['track']['artists'][0]['id'])
    return list_of_artists

def genres_occur_counter(genre_list):
    genreDict = {}
    for genre in genre_list:
        if (genre in genreDict):
            genreDict[genre] =  genreDict[genre] + 1
        else:
            genreDict[genre] = 1
    return genreDict

def get_total_genre_list(user):
    genrelist = []
    response = json.loads(requests.get("https://api.spotify.com/v1/users/{}/playlists?limit=3".format(user),headers=header).text)
    for playlist in response['items']:
        genrelist = genrelist + get_genre_from_artist_list(get_artist_list_from_playlist(playlist['id']))
    od =  genres_occur_counter(genrelist)          
    od2 = {}
    for key, value in sorted(od.items(), key=lambda item: item[1],reverse=True):
        od2[key] = value
    return od2
