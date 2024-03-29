from re import match
from typing import Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.http import QueryDict
import json, requests, base64
from . import spotify as sp
from . import mongo as m
from . import email_match as email
from . import match as match

#list of users allowed to gain access for developement page
authorized_users = ['k7lw','nitbaba','arcanebelal','newburyrn','12151060767']

#list of default profile pictures to choose from in profile settings
stock_profile_pics = [
    "https://data.whicdn.com/images/347068182/original.jpg?t=1595858693",
    "https://images.unsplash.com/photo-1579783483458-83d02161294e?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=428&q=80",
    "https://images.unsplash.com/photo-1525069011944-e7adfe78b280?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTExfHxwcm9maWxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1502173842631-25b37aac8b08?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjIwfHxwcm9maWxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1543005273-13a39e8e8ef2?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjMzfHxwcm9maWxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1507037298722-240d3390a736?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjM3fHxwcm9maWxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1542309667-2a115d1f54c6?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MzY3fHxwcm9maWxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://2.bp.blogspot.com/-Hm0h1XeY_LY/WtVhE8YkCwI/AAAAAAAAEb8/5VoowcGdywIIEV0OpXFTZVGENWL8ibO8QCLcBGAs/s1600/Flashing%2BAstronaut%2BWallpaper%2BEngine.jpg",
    "https://sagaswhat.com/wp-content/uploads/2017/02/yourname_top.jpg",
    ]

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
    if ('profile' in request.session):
        load_profile(request,m.find_user(request.session['profile']['username']))
    request.session['tracklist'] = []
    return render(request, 'home.html')


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: initializes oauth flow with spotify function                                 #
###################################################################################################

def login(request):
    if request.method == 'GET':
        return redirect(sp.oauth_login_redirect("user-top-read user-read-email user-read-private","http://localhost:8000/log_auth/"));


###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: finalizes oauth and saves the profile and token into the session/cookies     #
###################################################################################################

def log_auth(request):
    oauth_dict = sp.oauth_access_token(request.GET['code'], "http://localhost:8000/log_auth/")
    sp_json = sp.get_user_info(oauth_dict['access_token'])
    #creates empty profile to be filled from wither the database or as a new user
    request.session['profile'] = {}
    #if the user exists populate the profile in the session
    if (m.check_username(sp_json['id'])):
        m.set_access_token(sp_json['id'],oauth_dict['access_token'])
        m.set_refresh_token(sp_json['id'],oauth_dict['refresh_token'])
        load_profile(request,m.find_user(sp_json['id']))
    #if not create the profile in the database
    else:
        #if users spotify account doesnt have an image set one for them
        if (len(sp_json['images']) == 0):
            sp_json['images'] = [{'url': "https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png"}]
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
        #populates the session data with the users profile
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
        return render(request, 'profile.html',{'user_json':request.session['profile'],'profile_pic_list':stock_profile_pics})
    else:
        return render(request, 'home.html')

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: updates profile in the database                                              #
###################################################################################################

def profile_update(request):
    if ('profile' in request.session):
        match_pref = m.get_match_pref(request.session['profile']['username'])['match_pref']
        print(request.POST.getlist('gender_select'))
        if(len(request.POST.getlist('gender_select')[0]) > 0):
            m.set_gender(request.session['profile']['username'],request.POST.getlist('gender_select')[0])
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
        return redirect('/profile/' + request.session['profile']['username'])
    else:
        return render(request, 'home.html')

###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: Shows list of profiles that are connected to the database                    #
###################################################################################################


def development_page(request):
    if ('profile' in request.session and request.session['profile']['username'] in authorized_users):
        user_list = []
        for user in m.find_all():
            user_list.append(user)
        return render(request, 'dev.html', {'user_list':user_list})
    else:
        return render(request, 'unauthorized.html')

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: redirects to the clicked on users profile page                               #
###################################################################################################

def development_page_post(request, username):
    if request.method == 'POST':
        if ('profile' in request.session and request.session['profile']['username'] in authorized_users):
            user_json = m.find_user(username)
            return render(request, 'profile.html', {'user_json':user_json})
        else:
            return render(request, 'unauthorized.html')

###################################################################################################
# Request Type: Get                                                                               #
# Route Explination: Shows the matchmaking page for the use rin the current session               #
###################################################################################################

def match_making(request):
    if ('profile' in request.session):
        load_profile(request,m.find_user(request.session['profile']['username']))
        user_match_list = match.match_pref(request.session['profile']['username'])
        fav_user_list = []
        for username in request.session['profile']['favorite_users']:
            fav_user_list.append(m.find_user(username))
        return render(request, 'match_making.html', {'match_list': user_match_list,
                                                    'fav_list': fav_user_list})
    else:
        return render(request, 'home.html')

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: requests a match via email through the email module                          #
###################################################################################################


def request_match(request):
    if request.method == 'POST':
        if ('profile' in request.session):
            send_email = request.POST.getlist('match_email')
            email.sendemail(send_email,request.session['profile']['displayname'],request.session['profile']['email'])
            return redirect(match_making)
        else:
            return render(request, 'home.html')
    else:
        return redirect(match_making)

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: adds the selected profile to the session users favorite user list            #
###################################################################################################


def follow_match(request):
    if request.method == 'POST':
        if ('profile' in request.session):
            fav_user_list = m.get_favorite_users(request.session['profile']['username'])['favorite_users']
            if (not (request.POST.getlist('match_username')[0] in fav_user_list)):
                if (len(request.POST.getlist('match_username')[0]) > 0):
                    fav_user_list.append(request.POST.getlist('match_username')[0])
                    m.set_favorite_users(request.session['profile']['username'], fav_user_list)
            return redirect(match_making)     
        else:
            return render(request, 'home.html')
    else:
        return redirect(match_making)

###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: removes the selected profile to the session users favorite user list            #
###################################################################################################

def unfavorite_user(request):
    if request.method == 'POST':
        if ('profile' in request.session):
            fav_user_list = m.get_favorite_users(request.session['profile']['username'])['favorite_users']
            if (request.POST.getlist('unfavorite_username')[0] in fav_user_list):
                if (len(request.POST.getlist('unfavorite_username')[0]) > 0):
                    fav_user_list.remove(request.POST.getlist('unfavorite_username')[0])
                    m.set_favorite_users(request.session['profile']['username'], fav_user_list)
            return redirect(match_making)     
        else:
            return render(request, 'home.html')
    else:
        return redirect(match_making)


###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: changes the href url for the users profile picture                           #
###################################################################################################

def update_profile_pic(request):
    if request.method == 'POST':
        if ('profile' in request.session):
            profile_href = request.POST.getlist('profile_pic_selc')[0]
            m.set_profile_pic(request.session['profile']['username'],profile_href)
    return redirect('/profile/' + request.session['profile']['username'])


###################################################################################################
# Request Type: POST                                                                              #
# Route Explination: restores the users profile pic to the one they have on spotify               #
###################################################################################################
    
def restore_profile_pic(request):
    if request.method == 'POST':
        if ('profile' in request.session):
            try:
                profile_href = sp.get_user_info(request.session['profile']['access_token'])['images'][0]['url']
                m.set_profile_pic(request.session['profile']['username'],profile_href)
            except:
                pass
    return redirect('/profile/' + request.session['profile']['username'])