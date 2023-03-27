from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('processos', views.process_listing_page_view),
]
