from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from apps.operational_platform.forms import *
from apps.operational_platform.services import *
from main.models import QueueTask, UserProfile, QueueProcess, Team
from django.db.models import Q as Query


def businessExceptions_page_view(request):
    # User logado
    username = request.user.username
    processTaskDictionary = {}
    teamProcessList = []
    userProcessList = []
    userProfile = UserProfile.objects.filter(idUser__username=username).first()
    teamOfUser = None
    chefeEquipa = None
    userTaskCount = 0
    
    # PICK PROCESS IN OPERATIONAL PLATFORM
    if request.method == 'POST' and 'addProcess' in request.POST:
        addProcess(request, userProfile)

    # REMOVE PICKED PROCESS IN OPERATIONAL PLATFORM
    if request.method == 'POST' and 'removeProcess' in request.POST:
        removeProcess(request)

    if userProfile.idTeam is not None:
        teamOfUser = userProfile.idTeam
        teamOfUser1 = Team.objects.filter(id=teamOfUser.id).get()
        chefeEquipa = teamOfUser1.idTeamLider

    # PROCESS & TASKS MANAGER
    if (teamOfUser is not None) and (QueueProcess.objects.filter(idConfiguration__idTeam=teamOfUser).exists()):
        # ADDS THE PROCESSES TO x TEAM
        teamProcessList = addProcessToTeam(userProfile)

        # ADDS SPECIFIED PROCESS AND IT'S TASKS TO AN USER (THAT PICKED THE PROCESS)
        userTaskCount, userProcessList, processTaskDictionary = addProcessToUser(userProfile)

    # GET ALL USER FROM DATABASE
    allUsersDataBase = UserProfile.objects.all()

    # GET THE NUMBER OF TEAM PROCESSES
    teamProcessCount = len(teamProcessList)
    # QueueProcess.objects.filter(idConfiguration__idTeam=user_profile.idTeam).count()

    # GET THE NUMBER OF USER PROCESSES
    userProcessCount = len(userProcessList)


    context = {
        'teamName': teamOfUser,
        'teamProcesses': teamProcessList,
        'userProcesses': userProcessList,
        'chefeDeEquipa': str(chefeEquipa),
        'username': str(username),
        'nomeUsers': allUsersDataBase,
        'TeamProcessCount': teamProcessCount,
        'UserProcessCount': userProcessCount,
        'UserTaskCount': userTaskCount,
        'userTasks': processTaskDictionary
    }

    return render(request, 'operational_platform/businessExceptions.html', context)


def correcaoDocumentos_page_view(request, taskId):
    taskData = TaskData.objects.filter(Query(idTask=taskId)& Query(outputData = ""))
    task = QueueTask.objects.get(id = taskId)

    if request.method == 'POST':
        form = taskForm(request.POST, fields=getInputData(taskId))
        if form.is_valid():
            taskData[0].outputData = form.cleaned_data
            if len(taskData) == 1:
                task.state = 'Completed'
                task.save()
            
            cleanOutputData(task)
            return HttpResponseRedirect(reverse('businessExceptions'))

    else:
        form = taskForm(fields=getInputData(taskId))

    context = {
        'teamtasks': task,
        'form': form
    }

    return render(request, 'operational_platform/correcaoDocumentos.html', context)



def reportarErrosNoSistema_page_view(request):
    return render(request, 'operational_platform/reportarErrosNoSistema.html')


def changeSkills_page_view(request, userId):
    skillsObject = UserProfile.objects.get(id=userId)

    form = skillForm(request.POST or None, instance=skillsObject)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('businessExceptions'))

    context = {
        'form': form,
        'post_id': userId
    }

    return render(request, 'operational_platform/changeSkills.html', context)
