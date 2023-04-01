from django.shortcuts import render
from main.models import Task, Task_Configuration, TaskType

# Create your views here.

def businessExceptions_page_view(request):


	context = {
		'tasks': Task.objects.all(),
		'tasks_config':Task_Configuration.objects.all(),
		'tasks_type': TaskType.objects.all()
	}

	return render(request, 'operational_platform/businessExceptions.html', context)

def correcaoDocumentos_page_view(request):
	return render(request, 'operational_platform/correcaoDocumentos.html')

def reportarErrosNoSistema_page_view(request):
	return render(request, 'operational_platform/reportarErrosNoSistema.html')