import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main.models import UserProfile


# function that generates an E-mail code
def generatesEmailCode():
    length = 10
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))

    return result_str

# function that sends an email with a code in order to reset password
def sendEmailWithGeneratedCode(userEmailInput):
    code = generatesEmailCode()
    if not (verifyEmailOnDataBase(userEmailInput)):
        print("That email does not exist in the your database")
        return None


    # informações da conta
    email_utilizador = 'a22007237@alunos.ulht.pt'
    senha = 'JPcse1992'

    # informações do destinatário
    para = userEmailInput

    # informações do e-mail
    assunto = "Password reset code"
    mensagem = f'Here is the code u need to reset your password\n{code}'
    # criando mensagem
    msg = MIMEMultipart()
    msg['From'] = email_utilizador
    msg['To'] = para
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # conectando ao servidor SMTP
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()

    # fazendo login na conta
    server.login(email_utilizador, senha)

    # enviando o e-mail
    texto = msg.as_string()
    server.sendmail(email_utilizador, para, texto)

    # encerrando a conexão
    server.quit()

    # guardar na base de dados
    user_profile = UserProfile.objects.filter(user__email=userEmailInput).first()
    user_profile.recoveryCode = code
    user_profile.save()


def verifyEmailOnDataBase(userEmailInput):
    return UserProfile.objects.filter(user__email=userEmailInput).exists()


def validateCode(codeInput, userEmailInput):
    users = UserProfile.objects.filter(user__email=userEmailInput)
    if users.exists():
        user_profile = users.first()
        return user_profile.recoveryCode == codeInput
    else:
        return False


def changePassword(newPassword, userEmailInput):
    user_profile = UserProfile.objects.get(user__email=userEmailInput)
    user_profile.user.set_password(newPassword)
    user_profile.user.save()


