from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from apps.admin_platform.services import *
from main.models import *
from . forms import *


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


def adminGerirEquipaProcesso_view(request):
    allTeamsDataBase = Team.objects.all()
    allProcessConfigurationDataBase = ProcessConfiguration.objects.all()

    if request.method == 'POST':
        # FORMULARIO DE ALTERACAO DE EQUIPA DO PROCESSO
        if request.POST.get('teamProcessConfiguration'):
            changeProcessTeam(request)

    context = {
        'allTeamNames': allTeamsDataBase,
        'allProcessConfigurationNames': allProcessConfigurationDataBase,
    }

    return render(request, 'admin_platform/gerirEquipaProcesso.html', context)


def adminCriarTeams_view(request):

    criar_Team_Form = criarTeamForm(request.POST or None)

    if criar_Team_Form.is_valid():
        criar_Team_Form.save()
        return HttpResponseRedirect(reverse('criarTeams'))

    context = {
        'form': criar_Team_Form,
        'teams': Team.objects.all()
    }

    return render(request, 'admin_platform/criarTeams.html', context)

def adminTeams_delete_view(request, team_id):

    team = Team.objects.get(id=team_id)

    utilizadores = UserProfile.objects.all()
    allQueueTasks = QueueTask.objects.all()
    allProcesses = QueueProcess.objects.all()
    
    teamSize = 0 
    teamDoneProcess = False

    # VERIFY IF THE TEAM HAS ONLY THE TEAMLEADER AS A MEMBER
    for membros in utilizadores:
        if(membros.idTeam != None and membros.idTeam.id == team.id):
            teamSize += 1

    # VERIFY IF A TASK IN PROCESS WAS STARTED OR NOT, IF YES IT WONT LET ADMIN DELETE TEAM
    for task in allQueueTasks:
        for process in allProcesses:
            for membro in utilizadores:

                if not (process.idUser and membro.idTeam and task.idProcess.id == process.id and task.startWorkingDate):
                    continue
                
                if process.idUser.id == membro.idUser.id and membro.idTeam.id == team.id:
                    teamDoneProcess = True
                    break
            
            if teamDoneProcess:
                break

        if teamDoneProcess:
            break


    if(teamSize == 1 and (not teamDoneProcess)):
        get_Team_Form = Team.objects.get(id=team_id)
        get_Team_Form.delete()
        
    return HttpResponseRedirect(reverse('criarTeams'))



def adminCriarSkills_view(request):
    
    criar_Skill_Form = criarSkillForm(request.POST or None)

    if criar_Skill_Form.is_valid():
        criar_Skill_Form.save()
        return HttpResponseRedirect(reverse('criarSkills'))
    

    context = {
        'form': criar_Skill_Form,
        'skills': Skill.objects.all()
    }

    return render(request, 'admin_platform/criarSkills.html', context)


def adminSkills_delete_view(request, skill_id):

    utilizadores = UserProfile.objects.all()
    equipas = Team.objects.all()

    skillInUse = False

    # BOTH FOR's VERIFY IF THE SKILL WE WANT TO DELETE IS IN USE OR NOT

    for equipa in equipas:
        if equipa.idSkils.filter(id=skill_id).exists():
            skillInUse = True
            break

    for utilizador in utilizadores:
        if utilizador.idSkills.filter(id=skill_id).exists():
            skillInUse = True
            break


    if(not skillInUse):
        get_Skill_Form = Skill.objects.get(id=skill_id)
        get_Skill_Form.delete()

    return HttpResponseRedirect(reverse('criarSkills'))
