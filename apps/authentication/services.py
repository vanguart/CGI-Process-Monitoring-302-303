import random
import string
from main.models import User
from django.core.mail import send_mail

# function that generates an E-mail code
def generatesEmailCode(userEmailInput):
    userEmail = User.objects.filter(email=userEmailInput)

    if len(userEmail) == 0:
        print("there is nothing in the database")
        return None
      
    length = 10
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))

    return result_str

#function that sends an email with a code in order to reset password
def sendEmailWithGeneratedCode(userEmailInput):
    code = generatesEmailCode(userEmailInput)

    send_mail(
        'Reset Password',
        'Here is the code u need to reset your password\n {code}',
        'cgiprocessmonitor@gmail.com',
        ['88alexcosta88@gmail.com'],
    )