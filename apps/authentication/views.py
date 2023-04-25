from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.urls import reverse
from django.http import HttpResponseRedirect

from main.models import UserProfile
from .services import verifyEmailOnDataBase, sendEmailWithGeneratedCode, validateCode, changePassword
from datetime import timedelta
from django.utils import timezone


def login_page_view(request):
    if request.method == "POST":

        username_login_input = request.POST.get('username')
        password_login_input = request.POST.get('password')

        utilizador = authenticate(request,
                                  username=username_login_input,
                                  password=password_login_input
                                  )

        if utilizador is not None:

            login(request, utilizador)

            group = request.user.groups.filter(user=request.user)[0]

            if group.name == "Admin":
                return HttpResponseRedirect(reverse('todoAdmin'))
            elif group.name == "Analyst":
                return HttpResponseRedirect(reverse('todoAnalyst'))
            elif group.name == "Operational":
                return HttpResponseRedirect(reverse('businessExceptions'))

            # FALTA CRIAR PÁGINA QUE INDICA QUE O USER NÃO TEM GROUPNAME
            return HttpResponseRedirect(reverse('businessExceptions'))

        else:

            return render(
                request, 'authentication/login.html',
                {'message': "Credenciais Inválidas"}
            )

    return render(request, 'authentication/login.html')


def logout_page_view(request):
    logout(request)
    return render(request, 'authentication/login.html')


def recuperarPassword_page_view(request):
    if request.method == "POST":

        email_recover_input = request.POST.get('email')
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

        if validaMail:

            sendEmailWithGeneratedCode(email_recover_input)

            # REALIZA UM REQUEST DA SESSION (PEDINDO O EMAIL)
            request.session['email_recover_input'] = email_recover_input

            return render(request, 'authentication/recuperarPasswordCode.html')
        else:
            return render(
                request, 'authentication/recuperarPassword.html',
                {'message': mnsgErro}
            )

    return render(request, 'authentication/recuperarPassword.html')


def recuperarPasswordCode_page_view(request):
    # OBTEMOS O RESULTADO DO PEDIDO DA SESSION (EMAIL)
    email_recover_input = request.session.get('email_recover_input')

    if request.method == "POST":
        # timer do código
        user_profile = UserProfile.objects.filter(user__email=email_recover_input).first()
        if user_profile.lastCodeSentTime is not None:
            elapsed_time = timezone.now() - user_profile.lastCodeSentTime
            if elapsed_time > timedelta(minutes=5):
                user_profile.recoveryCode = ""
                user_profile.lastCodeSentTime = None
                user_profile.save()

        codigo_recover_input = request.POST.get('codigo')

        validaCodigo = False

        # COLOCAR AQUI FORMA DE VALIDAR O CODIGO PROVENIENTE DO EMAIL
        if validateCode(codigo_recover_input, email_recover_input):
            validaCodigo = True

        if validaCodigo:

            # REALIZA UM REQUEST DA SESSION (PEDINDO O EMAIL)
            request.session['email_recover_input'] = email_recover_input

            return render(request, 'authentication/recuperarPasswordPwUpdate.html')
        else:

            return render(
                request, 'authentication/recuperarPasswordCode.html', {'message': "Código Inválido"})

    return render(request, 'authentication/recuperarPasswordCode.html')


def recuperarPasswordPwUpdate_page_view(request):
    # OBTEMOS O RESULTADO DO PEDIDO DA SESSION (EMAIL)
    email_recover_input = request.session.get('email_recover_input')

    if request.method == "POST":

        new_password1_input = request.POST.get('password1')
        new_password2_input = request.POST.get('password2')
        validaPassword = False

        # COLOCAR AQUI FORMA DE VALIDAR AS PASSWORDS
        if new_password2_input == new_password1_input:
            validaPassword = True
            changePassword(new_password1_input, email_recover_input)

        if validaPassword:
            return render(request, 'authentication/login.html')
        else:
            return render(
                request, 'authentication/recuperarPasswordPwUpdate.html',
                {'message': "Password Incorreta"}
            )
    return render(request, 'authentication/recuperarPasswordPwUpdate.html')
