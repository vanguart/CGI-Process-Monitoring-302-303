from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page_view),
    path('login', views.login_page_view, name='login'),
    path('logout', views.logout_page_view, name='logout'),
    path('recuperarPassword', views.recuperarPassword_page_view, name='recuperarPassword'),
    path('recuperarPasswordCode', views.recuperarPasswordCode_page_view, name='recuperarPasswordCode'),
    path('recuperarPasswordPwUpdate', views.recuperarPasswordPwUpdate_page_view, name='recuperarPasswordPwUpdate'),
]
