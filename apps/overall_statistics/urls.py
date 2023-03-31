from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('todoAdmin/', views.todoAnalyst_page_view, name='todoAnalyst'),
]