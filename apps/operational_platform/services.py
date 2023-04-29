from main.models import UserProfile, QueueProcess, QueueTask


def addProcess(process_id, username_user):
    user_profile = UserProfile.objects.filter(idUser__username=username_user)
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=user_profile.first())


def removeProcess(process_id):
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=None)
    
    
def getInputData(queue_task_id,dados = False):
    task = QueueTask.objects.get(id=queue_task_id)
    data = str(task.inputData)
    fields =  []
    dataAfterProcessing = []
    groupData = data.split(";")
    for j in range(0,len(groupData)):
        individualData = groupData[j].split(":")
        fields.append(individualData[0])
        dataAfterProcessing.append(individualData[1])
    result = list(zip(fields, dataAfterProcessing))
    return result
