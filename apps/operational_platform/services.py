from main.models import UserProfile, QueueProcess


def addProcess(process_id, username_user):
    user_profile = UserProfile.objects.filter(idUser__username=username_user)
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=user_profile.first())


def removeProcess(process_id):
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=None)