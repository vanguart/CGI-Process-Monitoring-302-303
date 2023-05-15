from django.shortcuts import render
from apps.admin_platform.services import *
from main.models import *


# Create your views here.

def adminPage_view(request):
    allUsersDataBase = UserProfile.objects.all()
    countTask = countTasks(allUsersDataBase)
    context = {
        'allUsersNames': allUsersDataBase,
        'tasksDone': countTask[0],
        'tasksTodo': countTask[1]
    }

    return render(request, 'admin_platform/adminPage.html', context)


def adminGerirCargosUsers_view(request):
    allUsersDataBase = UserProfile.objects.all()
    allTeamsDataBase = Team.objects.all()
    allGroupsDataBase = Group.objects.all()

    if request.method == 'POST':
        # FORMULARIO DE ALTERACAO DE EQUIPA
        if request.POST.get('equipa'):
            changeTeam(request)

        # FORMULARIO DE ALTERACAO DE GRUPO 
        if request.POST.get('grupo'):
            changeGroup(request)

    context = {
        'allUsersNames': allUsersDataBase,
        'allTeamNames': allTeamsDataBase,
        'allGroupNames': allGroupsDataBase,
    }

    return render(request, 'admin_platform/gerirCargosUsers.html', context)


def adminGerirCargosTeams_view(request):
    allTeamsDataBase = Team.objects.all()
    allUsersDataBase = UserProfile.objects.all()

    if request.method == 'POST':
        # FORMULARIO DE ALTERACAO DE EQUIPA
        if request.POST.get('teamLider'):
            changeTeamLider(request)

    context = {
        'allUsersNames': allUsersDataBase,
        'allTeamNames': allTeamsDataBase,
    }

    return render(request, 'admin_platform/gerirCargosTeams.html', context)
