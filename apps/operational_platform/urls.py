from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('businessExceptions', views.businessExceptions_page_view, name='businessExceptions'),
    path('changeSkills/<int:userId>', views.changeSkills_page_view, name='changeSkills'),
    path('correcaoDocumentos/<int:taskId>/<int:taskPosition>', views.correcaoDocumentos_page_view, name='correcaoDocumentos',),
    path('reportarErrosNoSistema', views.reportarErrosNoSistema_page_view, name='reportarErrosNoSistema')
]