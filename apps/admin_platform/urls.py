from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('adminPage', views.adminPage_view, name='adminPage'),
    path('gerirCargosUsers', views.adminGerirCargosUsers_view, name='gerirCargosUsers'),
    path('gerirCargosTeams', views.adminGerirCargosTeams_view, name='gerirCargosTeams'),
    path('gerirEquipaProcesso', views.adminGerirEquipaProcesso_view, name='gerirEquipaProcesso'),
    path('criarTeams', views.adminCriarTeams_view, name='criarTeams'),
    path('criarTeams/<int:team_id>/', views.adminTeams_delete_view, name='criarTeam_delete'),
    path('criarSkills/', views.adminCriarSkills_view, name='criarSkills'),
    path('criarSkills/<int:skill_id>/', views.adminSkills_delete_view, name='criarSkills_delete'),
]