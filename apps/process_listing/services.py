from main.models import Process, Task


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
