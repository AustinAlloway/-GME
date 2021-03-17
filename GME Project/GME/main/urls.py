
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
    path('devp/', views.development_page_post, name='devp'),
]
