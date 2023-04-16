# Connection API Orchestrator
import io
import json
import os

import requests
import msoffcrypto
import pandas as pd

from main.models import UserProfile, Task, Log, LogType, Team, Process

# ------------------- Start connection ------------- #

passwd = 'RPA-process-monitoring'
config_file = r"docs\config.xlsx"

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
# ------------------- End connection --------------- #


# ------------------- Start Extract ---------------- #
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


# ------------------- End Extract ------------------ #

# ------------------- Start Transform -------------- #
def transformQueue(items):
    itemsQueue = []
    for item in items:
        itemsQueue = {
            'priority': item['Priority'],
            'state': item['Status'],
        }


def transformLog(logs):
    itemLog = []
    for log in logs:
        itemLog = {
            # ver dados dos logs
        }
        loadLog(itemLog)


def transformTask(tasks):
    itemTask = []
    for task in tasks:
        itemTask = {
            # ver dados dos logs
        }
        loadTask(itemTask)


def transformProcess(processes):
    itemProcess = []
    for process in processes:
        itemProcess = {
            # ver dados dos logs
        }
        loadProcess(itemProcess)


def transformRPA(rpas):
    itemRPA = []
    for rpa in rpas:
        itemRPA = {
            # ver dados dos logs
        }
        loadRPA(itemRPA)


# ------------------- End Transform ---------------- #

# ------------------- Start Load ------------------- #
def loadLog(itemLog):
    log = Log()
    log.save()


def loadTask(itemTask):
    task = Task()
    task.save()


def loadProcess(itemProcess):
    process = Process()
    process.save()


def loadRPA(itemRPA):
    rpa = UserProfile()
    rpa.save()
# ------------------- End Load --------------------- #

# -------------- Start Other functions ------------- #


def ChangeStateRPA():
    print("Hi")


def getTaskLog(taskRef):
    log = Log.objects.filter(task__id=taskRef).all()
    textLog = ""
    for logging in log:
        try:
            with logging.ficheiro.open('r') as file:
                conteudo = file.read()
                textLog += conteudo + '\n'
                print(conteudo)
        except Exception as e:
            print(f"Erro ao ler o arquivo {logging.ficheiro}: {e}")
    return textLog

# -------------- End Other functions --------------- #