
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-main'),
    path('sample_up/', views.sample_sub, name='home-sub'),
]
