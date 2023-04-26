from django.forms import ModelForm
from django import forms

from main.models import Skill, UserProfile
#from .models import 

from django.contrib.admin.widgets import FilteredSelectMultiple


# FALTA CRIAR TABELAS NA BASE DE DADOS PARA SE INSERIR OS DADOS
# COMPLETAR DEPOIS DA CRIACAO DA TABELA DA BD

class skillForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =  ['idSkills']

        idSkills=forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple(), to_field_name='name')
        

