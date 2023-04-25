from main.models import UserProfile, Task, Team


def addTask(task_id, username_user):
    user_profile = UserProfile.objects.filter(user__username=username_user)
    task = Task.objects.filter(id=task_id)
    task.user = user_profile
    teamOfUser = Team.objects.filter(members=user_profile)
    # del teamOfUser.tasks.objects.filter(task)


def removeTask(task_id, user):
    print("hi")
