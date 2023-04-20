import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main.models import Log, Task, UserProfile, Team
import schedule
import time


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

        if logs.logType.name == "Fatal Error":
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
    email = 'a22007237@alunos.ulht.pt'
    
    for team in Team.all():
        tarefas = len(team.tasks)
        body = "To-do today:\n "+ tarefas
        enviamail(email,subject,body)


# todos os dias envia os emails
schedule.every(24).hours.do(enviarEmailErro)
schedule.every(24).hours.do(enviarEmailTarefasRealizarToday)
schedule.every(24).hours.do(enviarEmailObjetivo(70))


while True:
    schedule.run_pending()
    time.sleep(1)
