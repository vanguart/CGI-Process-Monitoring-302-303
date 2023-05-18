import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import msoffcrypto
import pandas as pd

from main.models import Log, QueueTask, UserProfile, Team
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
    senha = credentials_df[credentials_df["Name"] == "password"]["Value"].iloc[0]

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
    for logs in Log.objects.all():
        subject = "Task with "
        if logs.logType.name == "Warning":
            subject += "Warning"

        if logs.logType.name == "Fatal Error":
            subject += "Fatal Error"

        for task in QueueTask.objects.all():

            if task == logs.task:
                body = "You have " + subject.lower()
                if task.user is not None:
                    email = task.user.user.email
                    enviamail(email, subject, body)


def enviarEmailTarefasRealizarToday():
    subject = "Tasks to-do Today"

    for team in Team.objects.all():
        email = team.idTeamLider.idUser.email
        tarefas = QueueTask.objects.filter(idProcess__idUser__idTeam=team).count()
        body = "Number of tasks the team has to do today:" + str(tarefas) + " tasks!"
        enviamail(email, subject, body)

