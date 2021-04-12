
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-main'),
    path('login/', views.login, name='login'),
    path('log_auth/', views.log_auth, name='log_auth'),
    path('logout/', views.logout, name='logout'),
    path('anon_genre_submit/', views.anon_genre_submit, name='anon_genre_submit'),
    path('profile/<str:name>', views.profile, name='profile'),
    path('dev/', views.development_page, name='dev'),
    path('devp/<str:username>', views.development_page_post, name='devp'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('match_making/', views.match_making, name='match_making'),
    path('request_match/', views.request_match, name='request_match'),
    path('follow_match/', views.follow_match, name='follow_match'),
    path('unfavorite_user/', views.unfavorite_user, name='unfavorite_user'),
]
