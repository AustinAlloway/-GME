from typing import Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.http import QueryDict
import json, requests, base64
from . import spotify as sp
from . import mongo as m

authorized_users = ['k7lw','nitbaba','arcanebelal','newburyrn','12151060767']

#####################################################################################
# Param: the default request object and user profiles json                          #
# Function: puts the profile from the parameter into the session                    #
# RETURNS: Nothing because the profile gets added to the session                    #
# ON FAIL: Nothing Happens                                                          #
#####################################################################################

def load_profile(request,profile_json):
    try:
        request.session['profile']['username'] = profile_json['username']
        request.session['profile']['displayname'] = profile_json['displayname']
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
        request.session['profile']['music_profile'] = profile_json['music_profile']
        return None
    except:
        return None


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
        return redirect(sp.oauth_login_redirect("user-top-read user-read-email user-read-private","http://k7lw.com:8000/log_auth/"));


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: finalizes oauth and saves the profile and token into the session/cookies     #
###################################################################################################

def log_auth(request):
    oauth_dict = sp.oauth_access_token(request.GET['code'], "http://k7lw.com:8000/log_auth/")
    print(oauth_dict)
    sp_json = sp.get_user_info(oauth_dict['access_token'])
    request.session['profile'] = {}
    if (m.check_username(sp_json['id'])):
        load_profile(request,m.find_user(sp_json['id']))
    else:
        profile_json = m.profile_formatter(username = sp_json['id'],
        display_name= sp_json['display_name'],
        spotify_username=sp_json['id'],
        sp_profile= sp_json['external_urls']['spotify'],
        access_token=oauth_dict['access_token'],
        refresh_token=oauth_dict['refresh_token'],
        email=sp_json['email'],
        profile_pic=sp_json['images'][0]['url'],
        age=18,
        gender='N/A',
        country=sp_json['country'],
        match_pref={
            'age_min': 18,
	        'age_max': 55,
	        'gender': [ 'Male', 'Female']
        },
        favorite_users=[],
        music_profile=[sp.get_music_profile_spotify(sp.get_top_track_list(oauth_dict['access_token']), oauth_dict['access_token'])],
        )
        m.add_user(profile_json)
        load_profile(request,profile_json=profile_json)
    request.session['profile']['access_token'] = oauth_dict['access_token']
    request.session['profile']['refresh_token'] = oauth_dict['refresh_token']
    request.session['profile']['username'] = sp_json['id']
    request.session['profile']['display_name'] = sp_json['display_name']
    request.session['profile']['email'] = sp_json['email']
    request.session['profile']['profile_pic'] = sp_json['images'][0]['url']
    request.session['profile']['country'] = sp_json['country']
    request.session['profile']['sp_profile'] = sp_json['external_urls']['spotify']
    request.session['profile']['music_profile'] = [sp.get_music_profile_spotify(sp.get_top_track_list(request.session['profile']['access_token']), request.session['profile']['access_token'])]

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

def profile(request, name):
    if ('profile' in request.session) and (name == request.session['profile']['username']):
        load_profile(request,m.find_user(request.session['profile']['username']))
        return render(request, 'profile.html',{'user_json':request.session['profile']})
    else:
        return render(request, 'home.html')

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: updates profile in the database                                              #
###################################################################################################

def profile_update(request):
    if ('profile' in request.session):
        match_pref = m.get_match_pref(request.session['profile']['username'])['match_pref']
        if(len(request.POST.getlist('gender')[0]) > 0):
            m.set_gender(request.session['profile']['username'],request.POST.getlist('gender')[0])
        try:
            age_int = int(request.POST.getlist('age')[0])
            if (len(request.POST.getlist('age')) > 0):
                m.set_age(request.session['profile']['username'],age_int)
        except:
            pass
        try:
            age_int = int(request.POST.getlist('pref_age_min')[0])
            if (len(request.POST.getlist('pref_age_min')) > 0):
                match_pref['age_min'] = age_int
        except:
            pass
        try:
            age_int = int(request.POST.getlist('pref_age_max')[0])
            if (len(request.POST.getlist('pref_age_max')) > 0):
                match_pref['age_max'] = age_int
        except:
            pass
        if(len(request.POST.getlist('pref_gender')) > 0):
            match_pref['gender'] = request.POST.getlist('pref_gender')
        m.set_match_pref(request.session['profile']['username'], match_pref)
        load_profile(request,m.find_user(request.session['profile']['username']))
        return render(request, 'profile.html',{'user_json':request.session['profile']})
    else:
        return render(request, 'home.html')



def development_page(request):
    if ('profile' in request.session and request.session['profile']['username'] in authorized_users):
        user_list = []
        for user in m.find_all():
            user_list.append(user)
        return render(request, 'dev.html', {'user_list':user_list})
    else:
        return render(request, 'unauthorized.html')


def development_page_post(request, username):
    if request.method == 'POST':
        if ('profile' in request.session and request.session['profile']['username'] in authorized_users):
            user_json = m.find_user(username)
            return render(request, 'profile.html', {'user_json':user_json})
        else:
            return render(request, 'unauthorized.html')