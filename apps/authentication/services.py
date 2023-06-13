import io
import random
import smtplib
import string
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import msoffcrypto
import pandas as pd
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
    resultStr = ''.join(random.choice(string.ascii_letters) for i in range(length))

    return resultStr


# function that sends an email with a code in order to reset password
def sendEmailWithGeneratedCode(userEmailInput):
    code = generatesEmailCode()
    if not (verifyEmailOnDataBase(userEmailInput)):
        print("That email does not exist in the your database")
        return None

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
    para = userEmailInput

    # informações do e-mail
    assunto = "Password reset code"
    mensagem = f'Here is the code u need to reset your password\n{code}'
    # criando mensagem
    msg = MIMEMultipart()
    msg['From'] = emailUtilizador
    msg['To'] = para
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # conectando ao servidor SMTP
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()

    # fazendo login na conta
    server.login(emailUtilizador, senha)

    # enviando o e-mail
    texto = msg.as_string()
    server.sendmail(emailUtilizador, para, texto)

    # encerrando a conexão
    server.quit()

    # guardar na base de dados
    userProfile = UserProfile.objects.filter(idUser__email=userEmailInput).first()
    userProfile.recoveryCode = code
    userProfile.lastCodeSentTime = timezone.now()
    userProfile.save()


def verifyEmailOnDataBase(userEmailInput):
    return UserProfile.objects.filter(idUser__email=userEmailInput).exists()


def validateCode(codeInput, userEmailInput):
    users = UserProfile.objects.filter(idUser__email=userEmailInput)
    if users.exists():
        userProfile = users.first()
        return userProfile.recoveryCode == codeInput and codeInput != ""
    else:
        return False


def changePassword(newPassword, userEmailInput):
    userProfile = UserProfile.objects.get(idUser__email=userEmailInput)
    userProfile.idUser.set_password(newPassword)
    userProfile.idUser.save()


def userAuthenticated(request):
    usernameLoginInput = request.POST.get('username')
    passwordLoginInput = request.POST.get('password')

    return authenticate(request, username=usernameLoginInput, password=passwordLoginInput)


def changePage(request, userAutheticated):
    url = ""
    if userAutheticated is not None:
        login(request, userAutheticated)
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


def validateEmail(emailRecoverInput):
    validaMail = True
    mnsgErro = ""

    try:
        validate_email(emailRecoverInput)
    except Exception:
        validaMail = False
        mnsgErro = "Email Inválido"

    if not verifyEmailOnDataBase(emailRecoverInput):
        validaMail = False
        mnsgErro = "Email inexistente"

    return [validaMail, mnsgErro]


def timerCode(emailRecoverInput):
    userProfile = UserProfile.objects.filter(idUser__email=emailRecoverInput).first()
    if userProfile.lastCodeSentTime is not None:
        elapsedTime = timezone.now() - userProfile.lastCodeSentTime
        if elapsedTime > timedelta(minutes=1):
            userProfile.recoveryCode = ""
            userProfile.lastCodeSentTime = None
            userProfile.save()


def validateChangePassword(request, emailRecoverInput):
    newPassword1Input = request.POST.get('password1')
    newPassword2Input = request.POST.get('password2')
    validaPassword = False

    # COLOCAR AQUI FORMA DE VALIDAR AS PASSWORDS
    if newPassword2Input == newPassword1Input:
        validaPassword = True
        changePassword(newPassword1Input, emailRecoverInput)

    return validaPassword
