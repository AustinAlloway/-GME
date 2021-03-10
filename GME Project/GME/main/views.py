from typing import Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.http import QueryDict
import json, requests, base64
from . import spotify as sp


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
    request.session['access_token'] = oauth_dict['access_token']
    request.session['profile'] = sp.get_user_info(oauth_dict['access_token'])
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

