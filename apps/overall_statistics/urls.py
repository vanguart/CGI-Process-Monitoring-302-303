from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('statistics', views.statistics_page_view, name='statistics'),
]