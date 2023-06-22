from main.models import Process, Task
import os
import tempfile
from django import template


def decode_utf8(value):
    return value.decode('utf-8')


# function that returns all processes in the data base acording to input parameters
def getAllProcessesInDB(InicialDate, EndDate, label, state, ):
    allLabels = False
    allDates = False
    allStates = False

    if label == "noTag":
        allLabels = True

    if InicialDate is None and EndDate is None:
        allDates = True

    if state == "noState":
        allStates = True

    if allLabels and allStates and allDates:
        return Process.objects.all()
    elif allLabels and allStates:
        return Process.objects.filter(data__ranges=[InicialDate, EndDate])
    elif allLabels:
        return Process.objects.filter(data__ranges=[InicialDate, EndDate]).filter(state=state)
    else:
        return Process.objects.filter(data__ranges=[InicialDate, EndDate]).filter(state=state).filter(label=label)


def getAllTasksInAProcesses(processId):
    process = Process.objects.get(idProcessConfiguration=processId)
    return process.objects.all()


def convert_log_to_txt(log_file):
    txt_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')

    with open(log_file.path, 'r') as log:
        # Lê o conteúdo do arquivo de log
        log_content = log.read()

        # Escreve o conteúdo no arquivo temporário .txt
        txt_file.write(log_content)

    txt_file.close()
    return txt_file.name
