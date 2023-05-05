from main.models import *

"""
def changeTeam(team_id, user_id):

    user_profile = UserProfile.objects.filter(id=user_id)
    print(f"{user_profile}")
    a = Team.objects.filter(idTeamLider = user_profile.id.first())
    if not a.exists() :
        user_profile.update(idTeam=team_id)
"""

# TODO JOAO & RICARDO (CORRIGIR ESTA PARTE PARA O TEAMLIDER - TEAMLIDER NAO ALTERA DE TEAM)
def changeTeam(team_id, user_id):
    user_profile = UserProfile.objects.filter(id=user_id)
    team_lider = Team.objects.get(id=team_id)
    print(f"{team_lider.idTeamLider}-------------{user_profile.first().id}" )
    if team_lider.idTeamLider == user_profile.first():
        user_profile.update(idTeam=team_id)