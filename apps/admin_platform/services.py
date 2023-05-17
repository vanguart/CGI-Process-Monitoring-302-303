from main.models import *


def changeTeam(request):
    teamId, userId = request.POST.get('equipa').split('-')
    userProfile = UserProfile.objects.filter(id=userId)
    liderDeOutraEquipe = Team.objects.filter(idTeamLider=userProfile.first().id).exclude(id=teamId).exists()
    if not liderDeOutraEquipe:
        userProfile.update(idTeam=teamId)


def changeGroup(request):
    groupId, userId = request.POST.get('grupo').split('-')
    userProfile = UserProfile.objects.filter(id=userId)
    userProfile.update(idGroupUser=groupId)


def changeTeamLider(request):
    teamId, userId = request.POST.get('teamLider').split('-')
    team = Team.objects.filter(id=teamId)
    team.update(idTeamLider=userId)


def countTasks(allUsersDataBase):
    tasksDone = {}
    tasksTodo = {}

    tasksDoneCount = 0
    tasksTodoCount = 0
    for user in allUsersDataBase:

        tasksDone.update({user.id: tasksDoneCount})
        tasksTodo.update({user.id: tasksTodoCount})

        for processo in QueueProcess.objects.filter(idUser=user.id):

            for task in QueueTask.objects.filter(idProcess=processo.id):

                if task.state == "Completed":  # tarefas realizadas

                    tasksDoneCount += 1
                    tasksDone.update({user.id: tasksDoneCount})

                elif task.state == "Stopped":  # tarefas a realizar

                    tasksTodoCount += 1
                    tasksTodo.update({user.id: tasksTodoCount})

        tasksDoneCount = 0
        tasksTodoCount = 0
    return [tasksDone, tasksTodo]
