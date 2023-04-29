from main.models import UserProfile, QueueProcess, QueueTask


def addProcess(process_id, username_user):
    user_profile = UserProfile.objects.filter(idUser__username=username_user)
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=user_profile.first())


def removeProcess(process_id):
    process = QueueProcess.objects.filter(id=process_id)
    process.update(idUser=None)
    
    
def getInputFields(queue_task_id):
    task = QueueTask.objects.get(id=queue_task_id)
    data = str(task.inputData)
    result =  []
    groupData = data.split(";")
    for j in range(0,len(groupData)):
        individualData = groupData[j].split(":")
        result.append(individualData[0])
    print(result) 
