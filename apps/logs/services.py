# Connection API Orchestrator
import io
import json

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
    users = json.loads(
        requests.get(creds['url'] + f"odata/Users",
                     headers=header).content.decode('utf-8'))['value']
    user_info = []
    for user in users:
        if user['UnattendedRobot'] is not None:
            user_info.append(user)
    transformRPA(user_info)


def getLogs():
    logs = requests.get(creds['url'] + "odata/RobotLogs", headers=header)
    logs = logs.json()['value']
    transformLog(logs)


def getTask(process_name):
    #fazer filtro com o nome
    jobs_endpoint = creds['url'] + "odata/Tasks"
    response = requests.get(jobs_endpoint, headers=header)
    if response.status_code != 200:
        raise Exception("Erro ao buscar jobs do Orchestrator")

    jobs = json.loads(response.content.decode('utf-8'))['value']
    process_jobs = [job for job in jobs if job['ReleaseName'] == process_name]
    transformTask(process_jobs)


def getProcess():
    response = requests.get(creds['url'] + 'odata/Processes', headers=header, )
    if response.status_code != 200:
        raise Exception("Erro ao buscar processos do Orchestrator")

    # Processa a resposta como um objeto JSON
    processos = json.loads(response.content.decode("utf-8"))["value"]
    transformProcess(processos)


# ------------------- End Extract ------------------ #

# ------------------- Start Transform -------------- #

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
    processos_info = []
    for processo in processes:
        processo_info = {
            "IsAttended": processo["IsAttended"],
            "Title": processo["Title"],
            "Description": processo["Description"],
            "Published": processo["Published"],
            "Arguments": processo["Arguments"]
        }
        processos_info.append(processo_info)
    loadProcess(processos_info)


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
    print("Mudar estado RPA")


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
