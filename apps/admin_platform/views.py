from django.shortcuts import render
from apps.admin_platform.services import *
from main.models import *


# Create your views here.

def adminPage_view(request):

    allUsersDataBase = UserProfile.objects.all()

    tasksDone = {}
    tasksTodo = {}

    tasksDoneCount = 0
    tasksTodoCount = 0


    for user in allUsersDataBase:

        tasksDone.update({user.id: tasksDoneCount})
        tasksTodo.update({user.id: tasksTodoCount})

        for processo in QueueProcess.objects.filter(idUser=user.id):

            for task in QueueTask.objects.filter(idProcess=processo.id):

                if task.state == "Completed": # tarefas realizadas 

                    tasksDoneCount += 1
                    tasksDone.update({user.id: tasksDoneCount})

                elif task.state == "Stopped": # tarefas a realizar 

                    tasksTodoCount += 1
                    tasksTodo.update({user.id: tasksTodoCount})

        tasksDoneCount = 0
        tasksTodoCount = 0


    context = {
        'allUsersNames': allUsersDataBase,
        'tasksDone': tasksDone,
        'tasksTodo': tasksTodo
    }

    return render(request, 'admin_platform/adminPage.html', context)



def adminGerirCargos_view(request):

    allUsersDataBase = UserProfile.objects.all()
    allTeamsDataBase = Team.objects.all()
    allGroupsDataBase = Group.objects.all()



    if request.method == 'POST':

        # FORMULARIO DE ALTERACAO DE EQUIPA
        if request.POST.get('equipa'):
            team_id, user_id_team = request.POST.get('equipa').split('-')
            changeTeam(team_id,user_id_team)

        # FORMULARIO DE ALTERACAO DE GRUPO 
        if request.POST.get('grupo'):
            group_id, user_id_group = request.POST.get('grupo').split('-')


    context = {
        'allUsersNames': allUsersDataBase,
        'allTeamNames': allTeamsDataBase,
        'allGroupNames':allGroupsDataBase,
    }

    return render(request, 'admin_platform/gerirCargos.html', context)