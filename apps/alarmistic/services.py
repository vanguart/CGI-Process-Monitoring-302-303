import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date,timedelta
import msoffcrypto
import pandas as pd
from asgiref.sync import sync_to_async
from django.db.models import Q as Query
from main.models import Log, QueueTask, Team, QueueProcess


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

@sync_to_async
def enviarEmailErro():
    subject = "Processes with error "
    userEmail = ""
    processosUtilizadorComErros = {}

    infoMail = [0,0,0]
    for log in Log.objects.all():
        for process in QueueProcess.objects.all():
            countWarnings = 0
            countErrors = 0
            if log.idProcess.id == process.id and process.idConfiguration.idTeam != None:
                userEmail = process.idConfiguration.idTeam.idTeamLider.idUser.email
                infoMail[2]=process.id
                arquivo = open(str(log.ficheiro), 'r')
                linhas = arquivo.readlines()
                mensagemErro = ""

                for linha in linhas:
                    if linha == 1:
                        continue

                    dados = linha.split("\t")
                    
                    if dados[2] == "Warn":
                        countWarnings+=1

                    if dados[2] == "Error":
                        mensagemErro+= dados[3] + "\n"
                        countErrors+=1
 
                    infoMail[0], infoMail[1] = countWarnings, countErrors
                    processosUtilizadorComErros.update({userEmail : infoMail})

                    arquivo.close()
                for key,values  in processosUtilizadorComErros.items():
                    email = key
                    nomeProc = QueueProcess.objects.get(id=values[2])
                    body = f"Instance {process.id} of {nomeProc.idConfiguration.name} has {values[1]} fatal errors and {values[0]} warnings"
                    if countErrors > 0 or countWarnings > 0:
                        if countErrors > 0:
                            body+=f"\n Error message: {mensagemErro}"
                        if not nomeProc.EmailWasSent:
                            enviamail(email, subject, body)
                            nomeProc.EmailWasSent=True
                            nomeProc.save()

@sync_to_async
def enviarEmailTarefasRealizarToday():
    subject = "Tasks to-do Today"
    today = date.today().day
    yesterday = date.today() - timedelta(days=1)
    

    for team in Team.objects.all():
        sendEmail=True
        if not team.EmailWasSent == None:
            if yesterday == team.EmailWasSent.date():
                team.EmailWasSent = None
                team.save()
                
            elif team.EmailWasSent.date().day == today:
                sendEmail=False
              
                
        if sendEmail:
            email = team.idTeamLider.idUser.email
            dateToday = date.today()
            dateYesterday = dateToday - timedelta(days=1)
            tasksTodayCount = QueueTask.objects.filter(Query(idProcess__idUser__idTeam=team)& Query(startDate__date=dateToday)).count()
            tasksTodayYesterday = QueueTask.objects.filter(Query(idProcess__idUser__idTeam=team)& Query(endDate__date=dateYesterday)).count()
                

            body = "Number of tasks the team has to do today:" + str(tasksTodayCount) + " tasks!\nNumber of tasks done by the team yesterday:" + str(tasksTodayYesterday) + " tasks!"
            enviamail(email, subject, body)
            team.EmailWasSent=date.today()
            team.save()
        

