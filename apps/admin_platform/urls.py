from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('adminPage', views.adminPage_view, name='adminPage'),
    path('gerirCargosUsers', views.adminGerirCargosUsers_view, name='gerirCargosUsers'),
    path('gerirCargosTeams', views.adminGerirCargosTeams_view, name='gerirCargosTeams')
]