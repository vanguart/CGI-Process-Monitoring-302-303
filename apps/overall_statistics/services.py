from main.models import Process, User, Logs


# function that calculate Statts state in a period of time
def calculateStattsState(beginning, end):
    countNumberProcessesRunning = numberOfProcessesInInputState(beginning, end, "running")
    countNumberProcessesWaiting = numberOfProcessesInInputState(beginning, end, "waiting")
    countNumberProcessesCompleted = numberOfProcessesInInputState(beginning, end, "completed")
    countNumberProcessesPaused = numberOfProcessesInInputState(beginning, end, "paused")

    return [countNumberProcessesRunning, countNumberProcessesWaiting, countNumberProcessesCompleted,
            countNumberProcessesPaused]


# function that calculate Statts in a period of time
def calculateStattsError(beginning, end):
    countNumberProcessesWarning = numberOfProcessesInInputError(beginning, end, "warning")
    countNumberProcessesFatalError = numberOfProcessesInInputError(beginning, end, "fatalError")

    return [countNumberProcessesWarning, countNumberProcessesFatalError]


# function that returns the number of processes in inputState
def numberOfProcessesInInputState(beginning, end, inputState):
    countNumberProcessesInInputState = 0
    process_set = Process.objects.filter(state=inputState)

    if process_set.count() == 0:
        print("there is nothing in the database")
        return None

    for i in process_set:
        if beginning <= i.idSLA.inicialDate & end >= i.idSLA.finalDate:
            countNumberProcessesInInputState += 1

    return countNumberProcessesInInputState


# function that returns the number of processes that had the erroType passed
def numberOfProcessesInInputError(beginning, end, erroType):
    # Here we have to go to the Logs to see which tasks have
    # a warning and only count those that belong to different processes
    logs_set = Logs.objects.all()
    guardarIdProcessos = set()
    countNumberProcessesInInputError = 0
    if logs_set.count() == 0:
        print("there is nothing in the database")
        return None

    for i in logs_set:
        if i.idTask.idProcess in guardarIdProcessos:
            continue
        elif i.idLogType.name == erroType:
            if beginning <= i.idSLA.inicialDate & end >= i.idSLA.finalDate:
                guardarIdProcessos.add(i.idTask.idProcess)
                countNumberProcessesInInputError += 1

    return countNumberProcessesInInputError
