from typing import Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.http import QueryDict
import json, requests, base64
from . import spotify as sp
from . import mongo as m


def load_profile(request,profile_json):
    request.session['profile']['username'] = profile_json['username']
    request.session['profile']['display_name'] = profile_json['display_name']
    request.session['profile']['spotify_username'] = profile_json['spotify_username']
    request.session['profile']['sp_profile'] = profile_json['sp_profile']
    request.session['profile']['access_token'] = profile_json['access_token']
    request.session['profile']['refresh_token'] = profile_json['refresh_token']
    request.session['profile']['email'] = profile_json['email']
    request.session['profile']['profile_pic'] = profile_json['profile_pic']
    request.session['profile']['age'] = profile_json['age']
    request.session['profile']['gender'] = profile_json['gender']
    request.session['profile']['country'] = profile_json['country']
    request.session['profile']['match_pref'] = profile_json['match_pref']
    request.session['profile']['favorite_users'] = profile_json['favorite_users']
    request.session['profile']['music_profile'] = ['music_profile']
    return ""


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: initializes the tracklist to 0 and renders homepage                          #
###################################################################################################

def home(request):
    request.session['tracklist'] = []
    return render(request, 'home.html')


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: initializes oauth flow with spotify function                                 #
###################################################################################################

def login(request):
    if request.method == 'GET':
        return redirect(sp.oauth_login_redirect("user-top-read user-read-email user-read-private","http://localhost/log_auth/"));


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: finalizes oauth and saves the profile and token into the session/cookies     #
###################################################################################################

def log_auth(request):
    oauth_dict = sp.oauth_access_token(request.GET['code'], "http://localhost/log_auth/")
    sp_json = sp.get_user_info(oauth_dict['access_token'])
    request.session['profile'] = {}
    if (m.check_username(sp_json['id'])):
        load_profile(request,m.find_user(sp_json['id']))
    else:
        m.profile_formatter(username = sp_json['id'],
        display_name= sp_json['display_name'],
        spotify_username=sp_json['id'],
        sp_profile= ''
        )
        m.add_user()
        
        
    print(oauth_dict)
    return render(request, 'home.html')

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: Flush out session data and login credentials to logout of spotify acc        #
###################################################################################################

def logout(request):
    if request.method == 'POST':
        request.session.flush()
    return render(request, 'home.html')


###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: get recommeded tracks based of info in this post from form data              #
###################################################################################################

def anon_genre_submit(request):
    request.session['tracklist'] = sp.get_recommended(request.POST.getlist('genre'))
    return render(request, 'home.html')
        

###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: initializes the tracklist to 0 and renders homepage                          #
###################################################################################################

def profile(request):
    if 'profile' in request.session:
        return render(request, 'profile.html')
    else:
        return render(request, 'home.html')


def testingpage(request):
    
    return render(request, 'dev.html')

def testingpagep(request):
    if request.method == 'POST':
        if(sp.is_valid_token(request.session['access_token'])):
            request.session['profile']['music_profile'] = sp.get_music_profile(sp.get_top_track_list(request.session['access_token']), request.session['access_token'])
        else:
            oauth_dict = sp.refresh_token(request.session['refresh_token'], "http://localhost/log_auth/")
            request.session['profile']['access_token'] = oauth_dict['access_token']
            request.session['profile']['refresh_token'] = oauth_dict['refresh_token']
            request.session['profile']['music_profile'] = sp.get_music_profile(sp.get_top_track_list(request.session['access_token']), request.session['access_token'])
    return render(request, 'dev.html')