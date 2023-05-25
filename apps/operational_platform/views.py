import os
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from apps.operational_platform.forms import *
from apps.operational_platform.services import *
from main.models import QueueTask, UserProfile, QueueProcess, Team
from django.db.models import Q as Query
from datetime import datetime


def businessExceptions_page_view(request):
    # User logado
    username = request.user.username
    processTaskDictionary = {}
    verificaStateTasksInProcess = {}
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

    # TO VERIFY IF THE TASKS INSIDE THE PROCESS, STARTED THE CORRECTION PROCESS
    # IF YES, USER CANT DESELECT THE PROCESS, IF NO IT IS POSSIBLE TO REMOVE THE PROCESS
    for proc in userProcessList:
        entrei = False

        for task in QueueTask.objects.filter(idProcess=proc.id):
            if task.state == "Running":
                verificaStateTasksInProcess.update({proc.id: False})
                entrei = True
        if not entrei:
            verificaStateTasksInProcess.update({proc.id: True})

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
        'userTasks': processTaskDictionary,
        'dicTasks': verificaStateTasksInProcess,

    }

    return render(request, 'operational_platform/businessExceptions.html', context)


def correcaoDocumentos_page_view(request, taskId, taskPosition):
    countTaskData = TaskData.objects.filter(Query(idTask=taskId) & Query(outputData="")).count()
    taskData = TaskData.objects.filter(Query(idTask=taskId) & Query(outputData=""))[taskPosition]
    task = QueueTask.objects.get(id=taskId)
    # Obtém o diretório base do projeto
    BASE_DIR = os.path.dirname(os.path.abspath('CGI-Process-Monitoring-302-303'))
    # Caminhos relativos aos arquivos
    input_file = os.path.join(BASE_DIR, 'static/files/MOCK_DATA_SMALL.xlsx')
    output_file = os.path.join(BASE_DIR, 'static/files/excel.pdf')
    # Chama a função para converter o arquivo
    excel_to_pdf_with_data_check(input_file, output_file)

    if task.startWorkingDate is None:
        task.startWorkingDate = datetime.now()
        task.save()

    if request.method == 'POST':

        form = taskForm(request.POST, fields=getInputData(taskId, taskPosition))

        if form.is_valid():
            taskData.outputData = form.cleaned_data
            taskData.save()

            createHumanLogs(task, taskData, request)
            cleanOutputData(taskData.id)
            # There is no more taskData to correct
            if countTaskData == 1:
                task.idProcess.state = 'Completed'
                task.idProcess.endDate = datetime.now()
                task.idProcess.save()
                task.endDate = datetime.now()
                task.state = 'Completed'
                task.save()
                return HttpResponseRedirect(reverse('businessExceptions'))

            return HttpResponseRedirect(reverse('correcaoDocumentos', kwargs={'taskId': task.id, 'taskPosition': 0}))

    else:
        form = taskForm(fields=getInputData(taskId, taskPosition))

    context = {
        'numberTasks': countTaskData - 1,
        'currentPosition': taskPosition,
        'teamtasks': task,
        'form': form,
        'file': "../../static/files/excel.pdf"}
    return render(request, 'operational_platform/correcaoDocumentos.html', context)


def reportarErrosNoSistema_page_view(request):

    criar_reportarErros_Form = ReportingErrosForm(request.POST or None, request.FILES)

    if criar_reportarErros_Form.is_valid():

        username = request.user.username
        userProfile = UserProfile.objects.get(idUser__username=username)
        criar_reportarErros_Form.instance.idUser = userProfile

        criar_reportarErros_Form.save()

        return HttpResponseRedirect(reverse('businessExceptions'))
 
    context = {
        'form': criar_reportarErros_Form,
    }
    return render(request, 'operational_platform/reportarErrosNoSistema.html', context)


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
