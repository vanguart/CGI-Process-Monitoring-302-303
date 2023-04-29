# CGI-Process-Monitoring-302-303<br>

## Trabalho realizado por :<br>
Alexandre Costa a22007578<br>
João Eleutério a22007237<br>
José Sobral a22005813<br>
Ricardo Cleto a22006526<br>

## Guião de instalação:<br>

1. Instalar Django:
```
Guião de instalação do Django: https://docs.djangoproject.com/en/4.2/topics/install/
```

2. Clonagem do projeto através do seguinte comando:
```
git clone https://github.com/josesobral22005813/CGI-Process-Monitoring-302-303
```

3. Abrir o projeto com o IDE preferencial.

3. Instalar dependencias no terminal do IDE atravéz dos seguintes comandos:
```
pip install requests
pip install msoffcrypto-tool
pip install pandas
pip install openpyxl
pip install schedule
```

4. Configurar o manage.py do projeto atravéz dos seguintes comandos:
```
python manage.py makemigrations
python manage.py migrate
```

5. Criar utilizador admin para o projeto:
```
python manage.py createsuperuser #Após este comando colocar as credências de preferencia.
```

6. Correr o servidor na máquina local através do seguinte comando:
```
python manage.py runserver
```

7. Aceder á página de admin através do browser com o seguinte url: 
```
http://127.0.0.1:8000/admin
```

8. Realizar o login na página de admin com as credencias especificadas no passo 5.

9. Entrar no objeto "Groups" e adicionar 3 grupos com os nomes “Admin”, “Analyst” e “Operational”.

Após os passos acima descritos, o projeto deverá encontrar-se instalado e pronto para desenvolvimento/testagem/análise.
