from django.shortcuts import render
from apps.operational_platform.services import addTask, removeTask
from main.models import QueueTask, UserProfile, QueueProcess


# DEBUGGING


def businessExceptions_page_view(request):

    team_tasks_list = []
    user_tasks_list = []
    objectIDToTransfer= -1

    # User logado
    username = request.user.username

    if request.method == 'POST' and 'addTask' in request.POST:
        objectIDToTransfer = request.POST.get('addTask')
        addTask(objectIDToTransfer, username)

    if request.method == 'POST' and 'removeTask' in request.POST:
        objectIDToTransfer = request.POST.get('removeTask')
        removeTask(objectIDToTransfer)


    # Nome da equipa do User logado
    user_profile = UserProfile.objects.filter(user__username=username).first()
    teamOfUser = user_profile.idTeam

    # Tarefas da equipa do User logado
    if (teamOfUser is not None) and (QueueProcess.objects.filter(idTeam=teamOfUser).exists()):
        for idProcessos in QueueProcess.objects.filter(idTeam=teamOfUser):
            for task in QueueTask.objects.filter(idProcess=idProcessos):
                if task.user is None:
                    team_tasks_list.append(task)
                if str(task.user) == str(username):
                    user_tasks_list.append(task)


    # ORDENA AS TASKS PELA PRIORIDADE (Maior para o mais pequeno em termos de priority)
    team_tasks_list.sort(key=lambda x: x.priority, reverse=True)

    userTaskCount = len(user_tasks_list)


    context = {
        'teamName': teamOfUser,
        'teamtasks': team_tasks_list,
        'userTasksCount': userTaskCount,
        'userTaskList': user_tasks_list,
    }

    return render(request, 'operational_platform/businessExceptions.html', context)


def correcaoDocumentos_page_view(request, teamtasks_id):
    taskGet = QueueTask.objects.get(id=teamtasks_id)

    context = {
        'teamtasks': taskGet
    }
    return render(request, 'operational_platform/correcaoDocumentos.html', context)


def reportarErrosNoSistema_page_view(request):
    return render(request, 'operational_platform/reportarErrosNoSistema.html')
