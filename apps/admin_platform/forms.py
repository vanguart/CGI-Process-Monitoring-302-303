from django.forms import ModelForm
from django import forms

from main.models import Team, Skill, UserProfile
from django.contrib.auth.models import Group, User

class criarTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name','description','idPermissions','idTeamLider','idSkils']

        labels = {
            'name': 'Nome da equipa',
            'description': 'Descrição',
            'idPermissions': 'Permissões',
            'idTeamLider': 'Lider de equipa',
            'idSkils': 'Skills',
        }
        

    #name = forms.CharField(max_length=256)
    #description = forms.CharField(max_length=100)
    #idPermissions = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple(), to_field_name='name')
    #idTeamLider = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    #idSkils = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple(), to_field_name='nameSkill')


class criarSkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

        labels = {
            'nameSkill': 'Nome da Skill',
        }