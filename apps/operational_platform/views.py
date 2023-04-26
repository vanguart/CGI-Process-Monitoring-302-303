from gc import get_objects
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from apps.operational_platform.forms import skillForm
from apps.operational_platform.services import addTask, removeTask
from main.models import QueueTask, UserProfile, QueueProcess, Team


# DEBUGGING


def businessExceptions_page_view(request):

    team_process_list = []
 
    process_task_dictionary = {}
    objectIDToTransfer= -1

    # User logado
    username = request.user.username

    
    user_profile = UserProfile.objects.filter(idUser__username=username).first()
    teamOfUser = user_profile.idTeam

    teamOfUser1 = Team.objects.filter(id=teamOfUser.id).get()
    #chefeEquipa = teamOfUser1.idTeamLider == username.id
    chefeEquipa = teamOfUser1.idTeamLider

    # Tarefas da equipa do User logado
    if (teamOfUser is not None) and (QueueProcess.objects.filter(idConfiguration__idTeam=teamOfUser).exists()):
        
        for processos in QueueProcess.objects.filter(idUser = user_profile.id):

            team_process_list.append(processos)

            for task in QueueTask.objects.filter(idProcess = processos.id):
                if process_task_dictionary.get(processos.id) == None:
                    process_task_list = []
                    process_task_list.append(task)
                else:
                    process_task_list = process_task_dictionary.get(processos.id)
                    process_task_list.append(task)
                process_task_dictionary.update({processos.id:process_task_list})

                
    allUsersDB = UserProfile.objects.all()

    """
    form = skillForm()

    if request.method == "POST":
        user_profile = UserProfile.objects.get(pk=pk)
        form = skillForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
    """
    
    


    # use a variável search_query em sua lógica de busca


    #userTaskCount = len(user_tasks_list)

    """
    if request.method == 'POST' and 'addTask' in request.POST:
        objectIDToTransfer = request.POST.get('addTask')
        addTask(objectIDToTransfer, username)

    if request.method == 'POST' and 'removeTask' in request.POST:
        objectIDToTransfer = request.POST.get('removeTask')
        removeTask(objectIDToTransfer)


    # Nome da equipa do User logado
    user_profile = UserProfile.objects.filter(idUser__username=username).first()
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
"""

    context = {
        'teamName': teamOfUser,
        'teamProcesses': team_process_list,
        #'userTasksCount': userTaskCount,
        'ProcessDictionary': process_task_dictionary,
        'chefeDeEquipa': str(chefeEquipa),
        'username':str(username),
        'nomeUsers':allUsersDB,
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


def changeSkills_page_view(request, user_id):
    post = UserProfile.objects.get(id=user_id)
    form = skillForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('businessExceptions'))
    

    context = {'form': form, 'post_id': user_id}
    return render(request, 'operational_platform/changeSkills.html', context)
