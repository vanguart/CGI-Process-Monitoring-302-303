
from django.shortcuts import render
from django.contrib.auth import logout


from .services import sendEmailWithGeneratedCode, validateCode, changePage, \
    userAuthenticated, validateEmail, timerCode, validateChangePassword


def login_page_view(request):
    if request.method == "POST":
        user_autheticated = userAuthenticated(request)
        return changePage(request, user_autheticated)

    return render(request, 'authentication/login.html')


def logout_page_view(request):
    logout(request)
    return render(request, 'authentication/login.html')


def recuperarPassword_page_view(request):
    if request.method == "POST":
        email_recover_input = request.POST.get('email')
        validate = validateEmail(email_recover_input)  # [0] Boolean, [1] Error message

        if validate[0]:
            sendEmailWithGeneratedCode(email_recover_input)
            # REALIZA UM REQUEST DA SESSION (PEDINDO O EMAIL)
            request.session['email_recover_input'] = email_recover_input

            return render(request, 'authentication/recuperarPasswordCode.html')
        else:
            return render(
                request, 'authentication/recuperarPassword.html',
                {'message': validate[1]}
            )

    return render(request, 'authentication/recuperarPassword.html')


def recuperarPasswordCode_page_view(request):
    # OBTEMOS O RESULTADO DO PEDIDO DA SESSION (EMAIL)
    email_recover_input = request.session.get('email_recover_input')

    if request.method == "POST":
        # timer code
        timerCode(email_recover_input)

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

        validaPassword = validateChangePassword(request, email_recover_input)

        if validaPassword:
            return render(request, 'authentication/login.html')
        else:
            return render(
                request, 'authentication/recuperarPasswordPwUpdate.html',
                {'message': "Password Incorreta"}
            )
    return render(request, 'authentication/recuperarPasswordPwUpdate.html')
