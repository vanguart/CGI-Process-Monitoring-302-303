from django.shortcuts import render
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

                if task.state == "Completed":  # tarefas a realizar

                    tasksDoneCount += 1
                    tasksDone.update({user.id: tasksDoneCount})

                elif task.state == "Stopped":  # tarefas realizadas

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
