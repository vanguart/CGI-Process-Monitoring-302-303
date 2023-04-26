from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('businessExceptions', views.businessExceptions_page_view, name='businessExceptions'),
    path('changeSkills/<int:user_id>', views.changeSkills_page_view, name='changeSkills'),
    path('correcaoDocumentos/<int:teamtasks_id>', views.correcaoDocumentos_page_view, name='correcaoDocumentos'),
    path('reportarErrosNoSistema', views.reportarErrosNoSistema_page_view, name='reportarErrosNoSistema')
]