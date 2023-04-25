from main.models import UserProfile, Task, Team


def addTask(task_id, username_user):
    user_profile = UserProfile.objects.filter(user__username=username_user)
    task = Task.objects.filter(id=task_id)
    task.update(user=user_profile.first())


def removeTask(task_id):
    task = Task.objects.filter(id=task_id)
    task.update(user=None)