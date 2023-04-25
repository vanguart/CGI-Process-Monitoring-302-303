from django.shortcuts import render
from main.models import Task, UserProfile, Process


# DEBUGGING


def businessExceptions_page_view(request):
    team_tasks_list = []
    user_tasks_list = []

    # User logado
    username = request.user.username
    # Nome da equipa do User logado
    user_profile = UserProfile.objects.filter(user__username=username).first()
    teamOfUser = user_profile.idTeam
    # Tarefas da equipa do User logado
    if (teamOfUser is not None) and (Process.objects.filter(idTeam=teamOfUser).exists()):
        for idProcessos in Process.objects.filter(idTeam=teamOfUser):
            for task in Task.objects.filter(idProcess=idProcessos):
                if task.user is None:
                    team_tasks_list.append(task)
                if str(task.user) == str(username):
                    user_tasks_list.append(task)

    # ORDENA AS TASKS PELA PRIORIDADE (Maior para o mais pequeno em termos de priority)
    team_tasks_list.sort(key=lambda x: x.priority, reverse=True)

    userTaskCount = len(user_tasks_list)

    # a = getTaskLogs(1)
    context = {
        'teamName': teamOfUser,
        'teamtasks': team_tasks_list,
        'userTasksCount': userTaskCount,
        'userTaskList': user_tasks_list
    }

    return render(request, 'operational_platform/businessExceptions.html', context)


def correcaoDocumentos_page_view(request, teamtasks_id):
    taskGet = Task.objects.get(id=teamtasks_id)

    context = {
        'teamtasks': taskGet
    }
    return render(request, 'operational_platform/correcaoDocumentos.html', context)


def reportarErrosNoSistema_page_view(request):
    return render(request, 'operational_platform/reportarErrosNoSistema.html')
