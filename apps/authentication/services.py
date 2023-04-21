import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import User

from main.models import User


# function that generates an E-mail code
def generatesEmailCode(userEmailInput):


    length = 10
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))

    return result_str


# function that sends an email with a code in order to reset password
def sendEmailWithGeneratedCode(userEmailInput):
    code = generatesEmailCode(userEmailInput)
    

    if not (verifyEmailOnDataBase(userEmailInput)):
        print("That email does not exist in the your database")
        return None

    # send_mail(
    #     'Reset Password',
    #     f'Here is the code u need to reset your password\n {code}',
    #     'cgiprocessmonitor@gmail.com',
    #     ['88alexcosta88@gmail.com'],
    # )
    # userEmailInput = 'jpcse1992@gmail.com'

    # informações da conta
    email_usuario = 'a22007237@alunos.ulht.pt'
    senha = 'JPcse1992'

    # informações do destinatário
    para = userEmailInput

    # informações do e-mail
    assunto = "Password reset code"
    mensagem = f'Here is the code u need to reset your password\n {code}'
    # criando mensagem
    msg = MIMEMultipart()
    msg['From'] = email_usuario
    msg['To'] = para
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

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


def verifyEmailOnDataBase(userEmailInput):
    userEmail = User.objects.filter(email=userEmailInput).exists()
    return userEmail

# def change_password(id_user, newpassword):
# preciso receber o id/email do utilizador
# procurar o utilizador  user = User.objects.fileter(id=id_user)
# alterar palavra-passe
