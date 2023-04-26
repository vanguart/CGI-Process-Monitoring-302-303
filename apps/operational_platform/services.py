from main.models import UserProfile, QueueTask, Team


def addTask(task_id, username_user):
    user_profile = UserProfile.objects.filter(user__username=username_user)
    task = QueueTask.objects.filter(id=task_id)
    task.update(user=user_profile.first())


def removeTask(task_id):
    task = QueueTask.objects.filter(id=task_id)
    task.update(user=None)