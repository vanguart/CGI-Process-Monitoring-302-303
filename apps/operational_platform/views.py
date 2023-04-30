from gc import get_objects
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from apps.operational_platform.forms import *
from apps.operational_platform.services import *
from main.models import QueueTask, UserProfile, QueueProcess, Team
from django.db.models import Q as Query


# DEBUGGING


def businessExceptions_page_view(request):
    team_process_list = []
    user_process_list = []
    process_task_dictionary = {}
    objectIDToTransfer = -1


    # User logado
    username = request.user.username

    user_profile = UserProfile.objects.filter(idUser__username=username).first()
    teamOfUser = None
    chefeEquipa = None

    # PICK PROCESS IN OPERATIONAL PLATFORM
    if request.method == 'POST' and 'addProcess' in request.POST:
        
        maxTaskNumber = QueueProcess.objects.filter(idUser=user_profile.id).count()
       
        if maxTaskNumber < 2:
            objectIDToTransfer = request.POST.get('addProcess')
            addProcess(objectIDToTransfer, username)

    # REMOVE PICKED PROCESS IN OPERATIONAL PLATFORM
    if request.method == 'POST' and 'removeProcess' in request.POST:
        objectIDToTransfer = request.POST.get('removeProcess')
        removeProcess(objectIDToTransfer)



    if user_profile.idTeam is not None:
        teamOfUser = user_profile.idTeam
        teamOfUser1 = Team.objects.filter(id=teamOfUser.id).get()
        # chefeEquipa = teamOfUser1.idTeamLider == username.id
        chefeEquipa = teamOfUser1.idTeamLider


    # PROCESS & TASKS MANAGER
    if (teamOfUser is not None) and (QueueProcess.objects.filter(idConfiguration__idTeam=teamOfUser).exists()):

        # ADDS THE PROCESSES TO x TEAM
        for processo in QueueProcess.objects.filter(idConfiguration__idTeam=user_profile.idTeam).exclude(state='Completed'):
            if processo.idUser == None:
                team_process_list.append(processo)
                
        # ADDS SPECIFIED PROCESS AND IT'S TASKS TO AN USER (THAT PICKED THE PROCESS)   
        for processo in QueueProcess.objects.filter(idUser=user_profile.id).exclude(state='Completed'): 
            user_process_list.append(processo)
            for task in QueueTask.objects.filter(idProcess=processo.id).exclude( Query(state='Completed') | Query(state='Pending')):
                if process_task_dictionary.get(processo.id) is None:
                    process_task_list = [task]
                else:
                    process_task_list = process_task_dictionary.get(processo.id)
                    process_task_list.append(task)
                process_task_dictionary.update({processo.id: process_task_list})
            


    # GET ALL USER FROM DATABASE
    allUsersDataBase = UserProfile.objects.all()

    # GET THE NUMBER OF TEAM PROCESSES
    TeamProcessCount = len(team_process_list) #QueueProcess.objects.filter(idConfiguration__idTeam=user_profile.idTeam).count()

    # GET THE NUMBER OF USER PROCESSES
    UserProcessCount = len(user_process_list)
    
    # GET THE NUMBER OF USER TASKS TO-DO
    UserTaskCount = sum(len(listTasks) for listTasks in process_task_dictionary.values())


    context = {
        'teamName': teamOfUser,
        'teamProcesses': team_process_list,
        'userProcesses': user_process_list,
        'chefeDeEquipa': str(chefeEquipa),
        'username': str(username),
        'nomeUsers': allUsersDataBase,
        'TeamProcessCount': TeamProcessCount,
        'UserProcessCount': UserProcessCount,
        'UserTaskCount':UserTaskCount,
        'userTasks':process_task_dictionary
    }

    """
    team_process_list = []
    user_task_list = []
    process_task_dictionary = {}
    objectIDToTransfer = -1

    # User logado
    username = request.user.username

    user_profile = UserProfile.objects.filter(idUser__username=username).first()
    teamOfUser = None
    chefeEquipa = None

    if user_profile.idTeam is not None:
        teamOfUser = user_profile.idTeam
        teamOfUser1 = Team.objects.filter(id=teamOfUser.id).get()
        # chefeEquipa = teamOfUser1.idTeamLider == username.id
        chefeEquipa = teamOfUser1.idTeamLider

        # Tarefas da equipa do User logado
        if (teamOfUser is not None) and (QueueProcess.objects.filter(idConfiguration__idTeam=teamOfUser).exists()):

            for processos in QueueProcess.objects.filter(idUser=user_profile.id):

                team_process_list.append(processos)

                for task in QueueTask.objects.filter(idProcess=processos.id):
                    if process_task_dictionary.get(processos.id) is None:
                        process_task_list = [task]
                    else:
                        process_task_list = process_task_dictionary.get(processos.id)
                        process_task_list.append(task)
                    process_task_dictionary.update({processos.id: process_task_list})


    if request.method == 'POST' and 'addTask' in request.POST:
        objectIDToTransfer = request.POST.get('addTask')
        addTask(objectIDToTransfer, username)

    if request.method == 'POST' and 'removeTask' in request.POST:
        objectIDToTransfer = request.POST.get('removeTask')
        removeTask(objectIDToTransfer)


    allUsersDB = UserProfile.objects.all()

    userProcessCount = QueueProcess.objects.filter(idUser=user_profile).count()
    print(userProcessCount)
    
    context = {
        'teamName': teamOfUser,
        'teamProcesses': team_process_list,
        'userProcessCount': userProcessCount,
        'ProcessDictionary': process_task_dictionary,
        'chefeDeEquipa': str(chefeEquipa),
        'username': str(username),
        'nomeUsers': allUsersDB,
        'userTaskList':
    }
"""
    return render(request, 'operational_platform/businessExceptions.html', context)


def correcaoDocumentos_page_view(request, task_id):

    task = QueueTask.objects.get(id=task_id)

    if request.method == 'POST':
        form = taskForm(request.POST, fields=getInputData(task_id))
        if form.is_valid():
            # Create a new QueueTask object and populate its fields with the form data
            task.outputData = form.cleaned_data
            task.state = 'Completed'
            task.save()
            cleanOutputData(task_id)
            return HttpResponseRedirect(reverse('businessExceptions'))

    else:
        form = taskForm(fields=getInputData(task_id))
            
    
    context = {
        'teamtasks': task,
        'form': form
    }

    return render(request, 'operational_platform/correcaoDocumentos.html', context)


def reportarErrosNoSistema_page_view(request):
    return render(request, 'operational_platform/reportarErrosNoSistema.html')


def changeSkills_page_view(request, user_id):

    skillsObject = UserProfile.objects.get(id=user_id)

    form = skillForm(request.POST or None, instance=skillsObject)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('businessExceptions'))

    context = {
        'form': form, 
        'post_id': user_id
    }

    return render(request, 'operational_platform/changeSkills.html', context)
