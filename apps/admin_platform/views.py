from django.shortcuts import render
from main.models import *


# Create your views here.

def adminPage_view(request):
    allUsersDataBase = UserProfile.objects.all()
    tasksDone = {}
    tasksTodo = {}

    for user in allUsersDataBase:
        for processo in QueueProcess.objects.filter(idUser=user.id):
            for task in QueueTask.objects.filter(idProcess=processo.id):
                if task.state == "Completed":  # tarefas a realizar
                    tasksCount = QueueTask.objects.filter(idUser=user.id, state="Completed").count()
                    tasksDone.update({user.id: tasksCount})
                elif task.state == "Stopped":  # tarefas realizadas
                    tasksCount = QueueTask.objects.filter(idUser=user.id, state="Stopped").count()
                    tasksTodo.update({user.id: tasksCount})

    context = {
        'allUsersNames': allUsersDataBase,
        'tasksDone': tasksDone,
        'tasksTodo': tasksTodo
    }

    return render(request, 'admin_platform/adminPage.html', context)
