# Connection API Orchestrator
import io
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import msoffcrypto
import pandas as pd

from main.models import UserProfile, Task, Log, LogType, Team

passwd = 'RPA-process-monitoring'
config_file = r".\CGI-Process-Monitoring-302-303\docs\config.xlsx"

decrypted_workbook = io.BytesIO()
with open(config_file, 'rb') as file:
    office_file = msoffcrypto.OfficeFile(file)
    office_file.load_key(password=passwd)
    office_file.decrypt(decrypted_workbook)

credentials_df = pd.read_excel(decrypted_workbook, engine='openpyxl')

creds = {
    "usernameOrEmailAddress": credentials_df[credentials_df["Name"] == "usernameOrEmailAddress"]["Value"].iloc[0],
    "password": credentials_df[credentials_df["Name"] == "password"]["Value"].iloc[0],
    "tenancyName": credentials_df[credentials_df["Name"] == "tenancyName"]["Value"].iloc[0],
    "grant_type": "refresh_token",
    "client_id": "8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
    "refresh_token": "2lRK1sYCtT3HA2g13WiBFJIOiETIDKOSfKtp9mgzuQuXo",
    'text-column': 'email',
    'id-column': 'id',
    'url': credentials_df[credentials_df["Name"] == "url"]["Value"].iloc[0],
}

header = {'content-type': 'application/json'}

r = requests.Session()

token = json.loads(r.post(
    'https://account.uipath.com/oauth/token',
    data=json.dumps(creds),
    headers=header, verify=False).content.decode('utf-8'))['access_token']

header['authorization'] = 'Bearer ' + token

header['X-UIPATH-TenantName'] = creds['tenancyName']


def ChangeStateRPA():
    print("Hi")


def addTaskQueue():
    print("Hi")


def removeTaskQueue():
    print("Hi")


# ------------------- Start Extract -----------------#
def getRPA():
    print("Hi")


def getLogs():
    logs = requests.get(
        creds['url'] + "odata/RobotLogs",
        headers=header)
    if logs.status_code == 200:
        # Extrai a lista de processos do corpo da resposta
        logs = logs.json()['value']
        for log in logs:
            print(log['Message'])
    else:
        print('Erro ao obter os logs dos robôs: %s', logs.text)


def getTask():
    print("Hi")


def getProcess():
    print("Hi")


def getQueue():
    items = requests.get(creds['url'] +
                         f'odata/QueueItems?$filter=QueueDefinitionId eq 761676',
                         headers=header)
    transformQueue(items)


# ------------------- End Extract -------------------#

# ------------------- Start Transform ---------------#
def transformQueue(items):
    processos = []
    for item in items:
        processo = {
            'priority': item['Priority'],
            'state': item['Status'],
        }
        loadQueue(processos.append(processo))


# ------------------- End Transform -----------------#

# ------------------- Start Load --------------------#

def loadQueue(process):
    task = Task()  # adicionar parametros
    task.save()


# ------------------- End Load ----------------------#

def criarItemQueue():
    print('hi')


def removerItemQueue():
    print('hi')


def enviamail(email, subject, body):
    # informações da conta
    email_usuario = 'a22007237@alunos.ulht.pt'
    senha = 'JPcse1992'

    # informações do destinatário
    para = email
    # criando mensagem
    msg = MIMEMultipart()
    msg['From'] = email_usuario
    msg['To'] = para
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # conectando ao servidor SMTP
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()

    # fazendo login na conta
    server.login(email_usuario, senha)

    # enviando o e-mail
    texto = msg.as_string()
    server.sendmail(email_usuario, para, texto)

    # encerrando a conexão
    server.quit()


# Fazer timer de enviar email diariamente

def enviarEmailErro():
    
    subject = "Task with "

    for logs in Log.objects.all():

        if logs.logType.name == "Warning":
            subject += "Warning"

        if logs.logType.name== "Fatal Error":
            subject += "Fatal Error"

        for task in Task.objects.all():

            if task == logs.task:
                body = "You have " + subject.lower()
                email = task.user.user.email
                enviamail(email, subject, body)


def enviarEmailObjetivo(threshold):
    subject = "Goal Low"
    for users in UserProfile.all():
        email = users.user.email
        if users.goal < threshold:
            if users.idPerfil == 'RPA':
                body = "The RPA " + users.user.name + " goal is low!"
                enviamail(email, subject, body)
            else:
                body = "Your goal is low!"
                enviamail(email, subject, body)


def enviarEmailTarefasRealizarToday():
    subject = "Tasks to-do Today"
    body = "To-do today:\n"

    # enviamail(email,subject,body)


enviarEmailErro()


