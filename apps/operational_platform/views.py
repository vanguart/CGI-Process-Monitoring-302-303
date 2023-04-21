from django.shortcuts import render
from main.models import Task, TaskConfiguration, TaskType, Team, UserProfile

# DEBUGGING


def businessExceptions_page_view(request):
	team_tasks_list = []
	user_tasks_list = []

	
	# User logado
	username = request.user.username

	#Nome da equipa do User logado
	teamOfUser = Team.objects.filter(members__user__username=username).first()
	
	#Tarefas da equipa do User logado
	if (teamOfUser != None) and (teamOfUser.tasks.exists()):
		
		teamTasks = teamOfUser.tasks.all()

		for task in teamTasks:
			if task.user == None:
				team_tasks_list.append(task)
			if str(task.user) == str(username):
				user_tasks_list.append(task)

	# ORDENA AS TASKS PELA PRIORIDADE (Maior para o mais pequeno em termos de priority)
	team_tasks_list.sort(key=lambda x: x.priority, reverse=True)
 
	userTaskCount = len(user_tasks_list)

	#a = getTaskLogs(1)
	context = {
		'teamName': teamOfUser,
		'teamtasks': team_tasks_list,
		'userTasksCount': userTaskCount,	
	}

	return render(request, 'operational_platform/businessExceptions.html', context)

def correcaoDocumentos_page_view(request):
	return render(request, 'operational_platform/correcaoDocumentos.html')

def reportarErrosNoSistema_page_view(request):
	return render(request, 'operational_platform/reportarErrosNoSistema.html')