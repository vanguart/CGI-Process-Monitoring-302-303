from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('adminPage', views.adminPage_view, name='adminPage'),
    path('gerirCargos', views.adminPage_view, name='gerirCargos')
]