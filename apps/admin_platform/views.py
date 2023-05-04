from django.shortcuts import render
from main.models import *
# Create your views here.

def adminPage_view(request):
	
	allUsersDataBase = UserProfile.objects.all()
	





	context = {
        'allUsersNames': allUsersDataBase,
    }

	return render(request, 'admin_platform/adminPage.html', context)