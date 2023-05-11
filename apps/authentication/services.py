import random
import smtplib
import string
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from main.models import UserProfile
from django.core.validators import validate_email


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
    user_profile = UserProfile.objects.filter(idUser__email=userEmailInput).first()
    user_profile.recoveryCode = code
    user_profile.lastCodeSentTime = timezone.now()
    user_profile.save()


def verifyEmailOnDataBase(userEmailInput):
    return UserProfile.objects.filter(idUser__email=userEmailInput).exists()


def validateCode(codeInput, userEmailInput):
    users = UserProfile.objects.filter(idUser__email=userEmailInput)
    if users.exists():
        user_profile = users.first()
        return user_profile.recoveryCode == codeInput and codeInput != ""
    else:
        return False


def changePassword(newPassword, userEmailInput):
    user_profile = UserProfile.objects.get(idUser__email=userEmailInput)
    user_profile.idUser.set_password(newPassword)
    user_profile.idUser.save()


def userAuthenticated(request):
    username_login_input = request.POST.get('username')
    password_login_input = request.POST.get('password')

    return authenticate(request, username=username_login_input, password=password_login_input)


def changePage(request,user_autheticated):
    url = ""
    if user_autheticated is not None:
        login(request, user_autheticated)
        if not request.user.groups.all():
            return render(request, 'authentication/contactAdmin.html')

        group = request.user.groups.filter(user=request.user)[0]
        if group.name == "Admin":
            url = 'adminPage'
        elif group.name == "Analyst":
            url = 'todoAnalyst'
        elif group.name == "Operational":
            url = 'businessExceptions'

        return HttpResponseRedirect(reverse(url))
    else:
        return render(
            request, 'authentication/login.html',
            {'message': "Credenciais Inválidas"}
        )


def validateEmail(email_recover_input):
    validaMail = True
    mnsgErro = ""

    try:
        validate_email(email_recover_input)
    except Exception:
        validaMail = False
        mnsgErro = "Email Inválido"

    if not verifyEmailOnDataBase(email_recover_input):
        validaMail = False
        mnsgErro = "Email inexistente"

    return [validaMail, mnsgErro]


def timerCode(email_recover_input):
    user_profile = UserProfile.objects.filter(idUser__email=email_recover_input).first()
    if user_profile.lastCodeSentTime is not None:
        elapsed_time = timezone.now() - user_profile.lastCodeSentTime
        if elapsed_time > timedelta(minutes=1):
            user_profile.recoveryCode = ""
            user_profile.lastCodeSentTime = None
            user_profile.save()


def validateChangePassword(request, email_recover_input):
    new_password1_input = request.POST.get('password1')
    new_password2_input = request.POST.get('password2')
    validaPassword = False

    # COLOCAR AQUI FORMA DE VALIDAR AS PASSWORDS
    if new_password2_input == new_password1_input:
        validaPassword = True
        changePassword(new_password1_input, email_recover_input)

    return validaPassword
