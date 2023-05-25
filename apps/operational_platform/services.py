from main.models import QueueProcess, QueueTask, TaskData, Log
from django.db.models import Q as Query
import win32com.client as win32
import pythoncom
from datetime import datetime
import pandas as pd
import os
from openpyxl import load_workbook


def addProcess(request, userProfile):
    maxTaskNumber = QueueProcess.objects.filter(idUser=userProfile.id).count()

    if maxTaskNumber < 2:
        objectIDToTransfer = request.POST.get('addProcess')
        process = QueueProcess.objects.filter(id=objectIDToTransfer)
        process.update(idUser=userProfile)


def removeProcess(request):
    objectIDToTransfer = request.POST.get('removeProcess')
    process = QueueProcess.objects.get(id=objectIDToTransfer)
    process.state = "Waiting"
    process.idUser = None
    process.save()


def getInputData(queueTaskId, taskPosition):
    task = QueueTask.objects.get(id=queueTaskId)
    taskData = TaskData.objects.filter(Query(idTask=task) & Query(outputData=""))[taskPosition]
    task.state = "Running"
    task.save()
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
        processo.state = "Running"
        processo.save()
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


def createHumanLogs(task, taskData, request):

    log = Log.objects.get(idProcess=task.idProcess)
    date = str(datetime.now())

    miliseconds = date.split(".")[1]

    if len(miliseconds) != 3:
        miliseconds = miliseconds[:3]

    miliseconds += "Z"

    timeStampTime = date.split(".")[0] + "." + miliseconds

    with open(log.ficheiro.path, 'a') as file:
       file.writelines(
           timeStampTime + "\t" + "Process Monitor" + "\t" + "Correction" + "\t" +"The user with id "
           + str(request.user.id) + "(" + request.user.username + ") completed the correction of the taskData with id = "
           + str(taskData.id) + "\t" + str(task.idProcess.id) + "\t" + task.idProcess.idConfiguration.name + "\n")


def adjust_column_width(ws):
    for column in ws.columns:
        max_length = 0
        column = list(column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # Ajuste para a largura desejada
        ws.column_dimensions[column[0].column_letter].width = adjusted_width


def adjust_column_width(ws):
    for column in ws.columns:
        max_length = 0
        column = list(column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # Ajuste para a largura desejada
        ws.column_dimensions[column[0].column_letter].width = adjusted_width


def excel_to_pdf(input_file, output_file):
    pythoncom.CoInitialize()
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(input_file)

    # Salvar o arquivo em formato PDF
    wb.ExportAsFixedFormat(0, output_file)

    # Fechar o arquivo e sair do Excel
    wb.Close()
    excel.Quit()


def excel_to_pdf_with_data_check(input_file, output_file):
    dataframe = pd.read_excel(input_file, usecols=[0, 1, 2, 3, 4])
    incomplete_rows = dataframe[dataframe.isnull().any(axis=1)]

    BASE_DIR = os.path.dirname(os.path.abspath('CGI-Process-Monitoring-302-303'))
    temp_file = os.path.join(BASE_DIR, 'static/files/teste2.xlsx')

    incomplete_rows.to_excel(temp_file, index=False)

    # Expandir as células da primeira linha
    wb = load_workbook(temp_file)
    ws = wb.active
    adjust_column_width(ws)
    wb.save(temp_file)
    wb.close()

    excel_to_pdf(temp_file, output_file)

    os.remove(temp_file)
