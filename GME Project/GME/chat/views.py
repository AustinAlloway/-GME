from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

from .models import Room

#############################################
# Initializes fake usernames for identities #
#############################################
fake = Faker()

###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: sets the rooms set to all available Room objects and renders                 #
#                    to 'chat' app index.html which is the "lobby"                                #
###################################################################################################
def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: sets the rooms to the specific room slug and renders                         #
#                    to 'chat' app room_detail.html which is the "chatroom" instance              #
###################################################################################################
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})

###################################################################################################
# Request Type: GET                                                                               #
# Route Explination: initializes the identity of the user and grants them access to twilio        #                 #
#                    credentials if correct to corresponding token of account instance            #
###################################################################################################
def token(request):
    identity = request.GET.get('identity', request.session['profile']['displayname'])
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)