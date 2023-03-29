from django.forms import ModelForm
from django import forms
#from .models import 

# FALTA CRIAR TABELAS NA BASE DE DADOS PARA SE INSERIR OS DADOS
# COMPLETAR DEPOIS DA CRIACAO DA TABELA DA BD

class reportarErroNoSistemaForm(ModelForm):
    class Meta:
        #COLOCAR NOME DA TABELA 
        #model = Post
        fields = '__all__'

        # ferramentas
        widgets = {
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'autor...'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'titulo...'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descricao...'}),

        }

        help_texts = {
            'autor': '↔ Insira neste campo o nome do autor',
            'titulo': '↔ Insira neste campo um titulo desejável',
            'descricao': '↔ Insira neste campo uma descrição a seu gosto',
            'link': '↔ Insira, somente se desejar, um link'
        }

        labels = {
            'autor': 'Autor',
            'titulo': 'Título',
            'descricao': 'Descrição',
            'link': 'Link que deseja inserir',
        }