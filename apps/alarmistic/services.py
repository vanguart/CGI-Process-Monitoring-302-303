import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import msoffcrypto
import pandas as pd

from main.models import Log, QueueTask, UserProfile, Team, QueueProcess
import schedule
import time


def enviamail(email, subject, body):
    passwd = 'RPA-process-monitoring'
    config_file = r"docs\config.xlsx"

    decrypted_workbook = io.BytesIO()
    with open(config_file, 'rb') as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=passwd)
        office_file.decrypt(decrypted_workbook)

    credentials_df = pd.read_excel(decrypted_workbook, engine='openpyxl')

    # informações da conta
    emailUtilizador = credentials_df[credentials_df["Name"] == "emailOutlook"]["Value"].iloc[0]
    senha = credentials_df[credentials_df["Name"] == "passwordOutlook"]["Value"].iloc[0]

    # informações do destinatário
    para = email
    # criando mensagem
    msg = MIMEMultipart()
    msg['From'] = emailUtilizador
    msg['To'] = para
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # conectando ao servidor SMTP
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()

    # fazendo login na conta
    server.login(emailUtilizador, senha)

    # enviando o e-mail
    texto = msg.as_string()
    server.sendmail(emailUtilizador, para, texto)

    # encerrando a conexão
    server.quit()


def enviarEmailErro():
    subject = "Processes with error "
    userEmail = ""
    processosUtilizadorComErros = {}
    countWarnings = 0
    countErrors = 0
    infoMail = [0,0,0]
    for log in Log.objects.all():
        for process in QueueProcess.objects.all():
                if log.idProcess.id == process.id and process.idUser != None:
                    userEmail = process.idUser.idUser.email

                    infoMail[2]=process.id

                    arquivo = open(str(log.ficheiro), 'r')
                    linhas = arquivo.readlines()

                    for linha in linhas:
                        if linha == 1:
                            continue

                        dados = linha.split("\t")
                        if dados[2] == "Warn":
                            countWarnings+=1

                        if dados[2] == "Error":
                            countErrors+=1

                        infoMail[0], infoMail[1] = countWarnings, countErrors
                        processosUtilizadorComErros.update({userEmail : infoMail})

                    arquivo.close()

    for key,values  in processosUtilizadorComErros.items():
        email = key
        nomeProc = QueueProcess.objects.get(id=values[2])
        body = f"In the process {nomeProc.idConfiguration.name} - has {values[1]} fatal errors; has {values[0]} warnings"
        enviamail(email, subject, body)


def enviarEmailTarefasRealizarToday():
    subject = "Tasks to-do Today"

    for team in Team.objects.all():
        email = team.idTeamLider.idUser.email
        tarefas = QueueTask.objects.filter(idProcess__idUser__idTeam=team).count()
        body = "Number of tasks the team has to do today:" + str(tarefas) + " tasks!"
        enviamail(email, subject, body)

