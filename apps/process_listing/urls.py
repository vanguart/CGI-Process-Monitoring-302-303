from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('process_listing', views.process_listing_page_view, name='process_listing')
]
