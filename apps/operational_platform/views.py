from django.shortcuts import render
from main.models import Task, TaskConfiguration, TaskType, Team, UserProfile

# DEBUGGING
from apps.logs.services import getTaskLogs


def businessExceptions_page_view(request):
	tasks_list = []
	# User logado
	username = request.user.username

	#Nome da equipa do User logado
	teamOfUser = Team.objects.filter(members__user__username=username).first()
	
	#Tarefas da equipa do User logado
	if (teamOfUser != None) and (teamOfUser.tasks.exists()):
		
		teamTasks = teamOfUser.tasks.all()

		for task in teamTasks:
			tasks_list.append(task)

	#a = getTaskLogs(1)
	context = {
		'teamName': teamOfUser,
		'teamtasks': tasks_list,
		#'a': a,
	}

	return render(request, 'operational_platform/businessExceptions.html', context)

def correcaoDocumentos_page_view(request):
	return render(request, 'operational_platform/correcaoDocumentos.html')

def reportarErrosNoSistema_page_view(request):
	return render(request, 'operational_platform/reportarErrosNoSistema.html')