from main.models import UserProfile, QueueProcess, QueueTask, TaskData
from django.db.models import Q as Query
import win32com.client as win32
import pythoncom


def addProcess(request, userProfile):
    maxTaskNumber = QueueProcess.objects.filter(idUser=userProfile.id).count()

    if maxTaskNumber < 2:
        objectIDToTransfer = request.POST.get('addProcess')
        process = QueueProcess.objects.filter(id=objectIDToTransfer)
        process.update(idUser=userProfile)


def removeProcess(request):
    objectIDToTransfer = request.POST.get('removeProcess')
    process = QueueProcess.objects.filter(id=objectIDToTransfer)
    process.update(idUser=None)


def getInputData(queueTaskId):
    task = QueueTask.objects.get(id=queueTaskId)
    taskData = TaskData.objects.filter(Query(idTask=task) & Query(outputData="")).first()

    data = str(taskData.inputData)  # type: ignore
    fields = []
    dataAfterProcessing = []
    groupData = data.split(";")
    for j in range(0, len(groupData)):
        individualData = groupData[j].split(":")
        fields.append(individualData[0])
        dataAfterProcessing.append(individualData[1])
    result = list(zip(fields, dataAfterProcessing))
    return result


def cleanOutputData(taskDataId):
    taskData = TaskData.objects.get(id=taskDataId)
    data = str(taskData.outputData)

    data = data.replace("{", "").replace("}", "").replace("\'", "")
    groupData = data.split(",")
    result = ""
    for j in range(0, len(groupData)):
        individualData = groupData[j].split(":")
        if j == 0:

            result = result + individualData[0].strip() + ":" + individualData[1].strip()
        else:
            result = result + ";" + individualData[0].strip() + ":" + individualData[1].strip()

    taskData.outputData = result
    taskData.save()


def addProcessToTeam(userProfile):
    teamProcessList = []
    for processo in QueueProcess.objects.filter(idConfiguration__idTeam=userProfile.idTeam).exclude(
            Query(state='Completed') | Query(state='Aborted')):
        if processo.idUser is None:
            teamProcessList.append(processo)

    return teamProcessList


def addProcessToUser(userProfile):
    userProcessList = []
    processTaskDictionary = {}
    userTaskCount = 0
    for processo in QueueProcess.objects.filter(idUser=userProfile.id).exclude(
            Query(state='Completed') | Query(state='Aborted')):
        userProcessList.append(processo)
        for task in QueueTask.objects.filter(idProcess=processo.id).exclude(
                Query(state='Completed') | Query(state='Aborted')):
            userTaskCount += TaskData.objects.filter(idTask=task.id, outputData='').count()

            if processTaskDictionary.get(processo.id) is None:
                processTaskList = [task]
            else:
                processTaskList = processTaskDictionary.get(processo.id)
                processTaskList.append(task)
            processTaskDictionary.update({processo.id: processTaskList})

    return userTaskCount, userProcessList, processTaskDictionary


def excel_to_pdf(input_file, output_file):
    pythoncom.CoInitialize()
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(input_file)

    # Salvar o arquivo em formato PDF
    wb.ExportAsFixedFormat(0, output_file)

    # Fechar o arquivo e sair do Excel
    wb.Close()
    excel.Quit()
