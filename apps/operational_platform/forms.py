from django.forms import ModelForm
from django import forms

from main.models import Skill, UserProfile, QueueTask
#from .models import 

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin import widgets

# FALTA CRIAR TABELAS NA BASE DE DADOS PARA SE INSERIR OS DADOS
# COMPLETAR DEPOIS DA CRIACAO DA TABELA DA BD

class skillForm(ModelForm):
    class Meta:
        model = UserProfile
        fields =  ['idSkills']

        idSkills=forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple(), to_field_name='name')
        

class taskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')
        super().__init__(*args, **kwargs)
        for i in fields:
            self.fields[i[0]] = forms.CharField(initial=i[1])

    class Meta:
        model = QueueTask
        fields = ['outputData']



