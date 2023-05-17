
from django.shortcuts import render
from django.contrib.auth import logout


from .services import sendEmailWithGeneratedCode, validateCode, changePage, \
    userAuthenticated, validateEmail, timerCode, validateChangePassword


def login_page_view(request):
    if request.method == "POST":
        userAutheticated = userAuthenticated(request)
        return changePage(request, userAutheticated)

    return render(request, 'authentication/login.html')


def logout_page_view(request):
    logout(request)
    return render(request, 'authentication/login.html')


def recuperarPassword_page_view(request):
    if request.method == "POST":
        emailRecoverInput = request.POST.get('email')
        validate = validateEmail(emailRecoverInput)  # [0] Boolean, [1] Error message

        if validate[0]:
            sendEmailWithGeneratedCode(emailRecoverInput)
            # REALIZA UM REQUEST DA SESSION (PEDINDO O EMAIL)
            request.session['email_recover_input'] = emailRecoverInput

            return render(request, 'authentication/recuperarPasswordCode.html')
        else:
            return render(
                request, 'authentication/recuperarPassword.html',
                {'message': validate[1]}
            )

    return render(request, 'authentication/recuperarPassword.html')


def recuperarPasswordCode_page_view(request):
    # OBTEMOS O RESULTADO DO PEDIDO DA SESSION (EMAIL)
    emailRecoverInput = request.session.get('email_recover_input')

    if request.method == "POST":
        # timer code
        timerCode(emailRecoverInput)

        codigoRecoverInput = request.POST.get('codigo')
        validaCodigo = False

        # COLOCAR AQUI FORMA DE VALIDAR O CODIGO PROVENIENTE DO EMAIL
        if validateCode(codigoRecoverInput, emailRecoverInput):
            validaCodigo = True

        if validaCodigo:
            # REALIZA UM REQUEST DA SESSION (PEDINDO O EMAIL)
            request.session['email_recover_input'] = emailRecoverInput

            return render(request, 'authentication/recuperarPasswordPwUpdate.html')
        else:

            return render(
                request, 'authentication/recuperarPasswordCode.html', {'message': "Código Inválido"})

    return render(request, 'authentication/recuperarPasswordCode.html')


def recuperarPasswordPwUpdate_page_view(request):
    # OBTEMOS O RESULTADO DO PEDIDO DA SESSION (EMAIL)
    emailRecoverInput = request.session.get('email_recover_input')

    if request.method == "POST":
        validaPassword = validateChangePassword(request, emailRecoverInput)

        if validaPassword:
            return render(request, 'authentication/login.html')
        else:
            return render(
                request, 'authentication/recuperarPasswordPwUpdate.html',
                {'message': "Password Incorreta"}
            )
    return render(request, 'authentication/recuperarPasswordPwUpdate.html')
