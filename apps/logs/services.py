# Connection API Orchestrator
import io
import os
import json
from asgiref.sync import sync_to_async
import requests
import msoffcrypto
import pandas as pd
from datetime import timedelta, datetime
from django.core.files import File
from django.db.models import Q

from main.models import QueueTask, Log, QueueProcess, ProcessConfiguration, ProcessType, TaskConfiguration, TaskData, \
    TaskType, Skill


# ------------------- Start connection ------------- #
@sync_to_async
def connectionToApi():
    passwd = 'RPA-process-monitoring'
    config_file = r"docs\config.xlsx"

    decrypted_workbook = io.BytesIO()
    with open(config_file, 'rb') as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=passwd)
        office_file.decrypt(decrypted_workbook)

    credentials_df = pd.read_excel(decrypted_workbook, engine='openpyxl')

    creds = {
        "usernameOrEmailAddress": credentials_df[credentials_df["Name"] == "usernameOrEmailAddress"]["Value"].iloc[0],
        "password": credentials_df[credentials_df["Name"] == "passwordGmail"]["Value"].iloc[0],
        "tenancyName": credentials_df[credentials_df["Name"] == "tenancyName"]["Value"].iloc[0],
        "grant_type": "refresh_token",
        "client_id": "8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
        "refresh_token": "2lRK1sYCtT3HA2g13WiBFJIOiETIDKOSfKtp9mgzuQuXo",
        'text-column': 'email',
        'id-column': 'id',
        'url': credentials_df[credentials_df["Name"] == "url"]["Value"].iloc[0],
    }

    header = {'content-type': 'application/json'}

    r = requests.Session()

    token = json.loads(r.post(
        'https://account.uipath.com/oauth/token',
        data=json.dumps(creds),
        headers=header, verify=False).content.decode('utf-8'))['access_token']

    header['authorization'] = 'Bearer ' + token

    header['X-UIPATH-TenantName'] = creds['tenancyName']

    header['X-UIPATH-OrganizationUnitId'] = '4500630'

    getLogs(creds, header)


# ------------------- End connection --------------- #


# ------------------- Start Extract ---------------- #


def getLogs(creds, header):
    jobs = requests.get(creds['url'] + "/odata/Jobs", headers=header)
    jobscount = jobs.json()['@odata.count']
    keys = []
    for i in range(0, jobscount):
        # we just get the logs of not running jobs
        if not jobs.json()['value'][i]['State'] == 'Running':
            keys.append(jobs.json()['value'][i]['Key'])

    transformLog(creds, header, keys)


# ------------------- End Extract ------------------ #

# ------------------- Start Transform -------------- #

def transformLog(creds, header, keys):
    file_path = "apps/logs/logData/jobkeys.txt"
    if not os.path.exists(file_path):
        fileread = open(file_path, "x")

    fileread = open(file_path, "r")
    lines = fileread.readlines()
    knowKeys = []

    for line in lines:
        knowKeys.append(line.strip())

    newKeys = list(set(keys).difference(knowKeys))

    # each key represents a new queueProcess
    for key in newKeys:

        key = str(key)
        skipThisProcess = False
        newOrOldProcessConfiguration = None
        newOrOldTaskConfiguration = None
        newQueueProcess = None
        newQueueTask = None
        queueTaskDoneByHuman = None
        priority = None
        allQueueTasksByQueueProcess = []

        logsTrace = requests.get(creds['url'] + f"/odata/RobotLogs?$filter=JobKey eq {key} and Level eq 'Trace'",
                                 headers=header)
        countLogsTrace = logsTrace.json()['@odata.count']

        for logTrace in range(0, countLogsTrace):

            jsonSplitMessageLog = str(logsTrace.json()['value'][logTrace]['Message']).split(";")

            if len(jsonSplitMessageLog) != 6:
                continue

            if jsonSplitMessageLog[0] == 'Process':
                # call loadLogProcessConfiguration
                _, processType, processName, description, maxTimeOfExecution, skills = jsonSplitMessageLog
                newOrOldProcessConfiguration, newQueueProcess = loadLogProcess(processType, processName, description,
                                                                               maxTimeOfExecution, skills)

                timeStamp = str(logsTrace.json()['value'][logTrace]['TimeStamp'])
                saveTimes = getTimeStamp(timeStamp)
                newQueueProcess.startDate = saveTimes[0] + " " + saveTimes[1]  # type: ignore
                newQueueProcess.registerDate = datetime.now()
                newQueueProcess.save()
                break

        # There was no log Process so nothing is going to be added in your database
        if newOrOldProcessConfiguration is None:
            return

        # There was no log Process so nothing is going to be added in your database
        if newQueueProcess is None:
            return

        logsError = requests.get(creds['url'] + f"/odata/RobotLogs?$filter=JobKey eq {key} and Level eq 'Error'",
                                 headers=header)

        countLogsError = logsError.json()['@odata.count']

        for logError in range(0, countLogsError):
            timeStamp = str(logsError.json()['value'][logError]['TimeStamp'])
            saveTimes = getTimeStamp(timeStamp)
            newQueueProcess.endDate = newQueueProcess.startDate  # type: ignore
            newQueueProcess.state = "Aborted"
            newQueueProcess.save()
            skipThisProcess = True

        # There is atleats 1 error so no tasks are going to me created or inserted in our database
        if not skipThisProcess:

            for logTrace in range(0, countLogsTrace):

                jsonSplitMessageLog = str(logsTrace.json()['value'][logTrace]['Message']).split(";")

                if len(jsonSplitMessageLog) != 6:
                    continue

                if jsonSplitMessageLog[0] == 'Task':
                    # call loadLogTaskConfiguration
                    _, taskType, taskName, description, maxTimeOfExecution, priority = jsonSplitMessageLog
                    newOrOldTaskConfiguration, newQueueTask = loadLogTaskConfiguration(newOrOldProcessConfiguration,
                                                                                       taskType, taskName, description,
                                                                                       maxTimeOfExecution,
                                                                                       newQueueProcess, priority)
                    allQueueTasksByQueueProcess.append(newQueueTask)

                    timeStamp = str(logsTrace.json()['value'][logTrace]['TimeStamp'])
                    saveTimes = getTimeStamp(timeStamp)
                    newQueueTask.startDate = saveTimes[0] + " " + saveTimes[1]  # type: ignore
                    newQueueTask.startWorkingDate = datetime.now()
                    newQueueTask.save()

            # There was no log Task so nothing is going to be added in your database
            if priority == None:
                return

                # There was no log Task so nothing is going to be added in your database
            if newOrOldTaskConfiguration == None:
                return

                # There was no log Task so nothing is going to be added in your database
            if newQueueTask == None:
                return

            # Check if any of the queueTaksk in the queueProcess needs to be done by Human
            for queueTasksByQueueProcess in allQueueTasksByQueueProcess:
                if queueTasksByQueueProcess.idTaskConfiguration.responsibility == "HUMANO":
                    queueTaskDoneByHuman = queueTasksByQueueProcess

            logsInfo = requests.get(creds['url'] + f"/odata/RobotLogs?$filter=JobKey eq {key} and Level eq 'Info'",
                                    headers=header)
            countLogsInfo = logsInfo.json()['@odata.count']

            # There was no log Task for  the Human to check so we skip the insert of the task data since we are not going to check it
            if not queueTaskDoneByHuman == None:

                for logInfo in range(0, countLogsInfo):

                    # Data to insert into taskData
                    jsonMessageLog = str(logsInfo.json()['value'][logInfo]['Message'])

                    jsonMessageLogSplit = jsonMessageLog.split(":")

                    if len(jsonMessageLogSplit) == 1:
                        continue

                    # The queueTaskDoneByHuman is the queueTask corresponding to the human that in this case is not going to work since there was no error or warning (just info)
                    # so this is the queueTasks where the robot data is going to be store
                    # there will be a lot of task data instance that corresponde to all the data extrated by the rpa

                    TaskData.objects.create(
                        idTask=queueTaskDoneByHuman,
                        inputData=jsonMessageLog,
                        outputData=jsonMessageLog,
                    )

                logsWarning = requests.get(
                    creds['url'] + f"/odata/RobotLogs?$filter=JobKey eq {key} and Level eq 'Warn'", headers=header)
                countLogsWarning = logsWarning.json()['@odata.count']

                # There is atleast 1 warning in this queueProcess
                if countLogsWarning != 0:

                    # Process is waiting since there was a warning and no Human is currently correcting the queueTask
                    newQueueProcess.state = "Waiting"
                    newQueueProcess.endDate = None
                    newQueueProcess.save()

                    # The QueueTasks that is done by Humans is waiting since there was a warning and no Human is correcting the queueTask
                    queueTaskDoneByHuman.state = "Waiting"
                    queueTaskDoneByHuman.startWorkingDate = None
                    queueTaskDoneByHuman.save()

                # There was no warning so the end date is the same of the start date 
                else:
                    queueTaskDoneByHuman.endDate = queueTaskDoneByHuman.startDate
                    queueTaskDoneByHuman.save()
                    newQueueProcess.endDate = queueTaskDoneByHuman.startDate
                    newOrOldProcessConfiguration.latestOperation = queueTaskDoneByHuman.startDate
                    newQueueProcess.save()
                    newOrOldProcessConfiguration.save()

                for logWarn in range(0, countLogsWarning):

                    # Data to insert into taskData
                    jsonMessageLogSplit = str(logsWarning.json()['value'][logWarn]['Message']).split("|")

                    # warning log is incorrect
                    if len(jsonMessageLogSplit) != 2:
                        continue

                    # The queueTaskDoneByHuman is the queueTask corresponding to the human that in this case is not going to work since there was no error or warning (just info)
                    # so this is the queueTasks where the robot data is going to be store
                    # there will be a lot of task data instance that corresponde to all the data extrated by the rpa

                    TaskData.objects.create(
                        idTask=queueTaskDoneByHuman,
                        inputData=jsonMessageLogSplit[1].strip(),
                        errorMessage=jsonMessageLogSplit[0].strip()
                    )

                # Now we are going to set the endDates to AllQueueTasks except the last which is done by the Human
                allQueueTasksByQueueProcessObjects = QueueTask.objects.filter(
                    id__in={instance.id for instance in allQueueTasksByQueueProcess})
                sortedTasksByStartedDate = allQueueTasksByQueueProcessObjects.order_by("startDate")

                for queueTask in range(0, len(sortedTasksByStartedDate) - 1):
                    sortedTasksByStartedDate[queueTask].endDate = sortedTasksByStartedDate[queueTask + 1].startDate
                    sortedTasksByStartedDate[queueTask].save()

        createLogFiles(creds, key, header, newQueueProcess)

    filewrite = open("apps/logs/logData/jobkeys.txt", "a")
    for key in newKeys:
        filewrite.write(key + "\n")


# ------------------- End Transform ---------------- #

# ------------------- Start Load ------------------- #
def loadLogProcess(processType, processName, description, maxTimeOfExecution, skills):
    processTypeDB = ProcessType.objects.filter(name=processType)
    # this ProcessType does not exit in our database so we are going to create it
    if len(processTypeDB) == 0:
        ProcessType.objects.create(name=processType)

    processTypeDB = ProcessType.objects.get(name=processType)

    processConfigurationDB = ProcessConfiguration.objects.filter(name=processName)
    # this ProcessConfiguration does not exit in our database so we are going to create it
    if len(processConfigurationDB) == 0:
        try:
            hours, minutes, seconds = maxTimeOfExecution.split(":")
            duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

            skills = skills.split(",")

            process_config = ProcessConfiguration.objects.create(
                name=processName,
                idProcessType=processTypeDB,
                description=description,
                maxTimeKPI=duration,
            )

            for skill in skills:

                skillsDB = Skill.objects.filter(nameSkill=skill)

                # this skill does not exit in our database so we are going to create it
                if len(skillsDB) == 0:
                    Skill.objects.create(nameSkill=skill)

                process_config.idSkills.add(Skill.objects.get(nameSkill=skill))
            process_config.save()

        except  Exception as e:
            print(str(e))

    processConfigurationDB = ProcessConfiguration.objects.get(name=processName)
    # creation of queueProcess
    queueProcessDB = QueueProcess.objects.create(idConfiguration=processConfigurationDB)

    return processConfigurationDB, queueProcessDB


def loadLogTaskConfiguration(processConfiguration, taskType, taskName, description, maxTimeOfExecution, queueProcess,
                             priority):
    taskTypeDB = TaskType.objects.filter(name=taskType)
    # this TaskType does not exit in our database so we are going to create it
    if len(taskTypeDB) == 0:
        TaskType.objects.create(name=taskType)

    taskTypeDB = TaskType.objects.get(name=taskType)

    taskConfigurationDB = TaskConfiguration.objects.filter(name=taskName)

    # this TaskConfiguration does not exit in our database so we are going to create it
    if len(taskConfigurationDB) == 0:
        hours, minutes, seconds = maxTimeOfExecution.split(":")
        duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        responsibility, description = description.split("-")

        TaskConfiguration.objects.create(
            idProcessConfiguration=processConfiguration,
            name=taskName,
            idtaskType=taskTypeDB,
            description=description,
            maxTimeKPI=duration,
            responsibility=responsibility
        )

    taskConfigurationDB = TaskConfiguration.objects.get(name=taskName)

    queueTaskDB = QueueTask.objects.create(
        idTaskConfiguration=taskConfigurationDB,
        idProcess=queueProcess,
        priority=priority
    )

    return taskConfigurationDB, queueTaskDB


# ------------------- End Load --------------------- #

# -------------- Start Other functions ------------- #

def getTimeStamp(timeStamp):
    startDay = timeStamp.split("T")[0]
    startHour = timeStamp.split("T")[1]
    return startDay, startHour


def createLogFiles(creds, key, header, newQueueProcess):
    # Write logs in our logs

    file_path = "apps/logs/logData/teste.txt"

    if os.path.exists(file_path):
        os.remove(file_path)

    # First we need to create a new txt file with some name that does not matter since its going to change when the los is created
    newLogTxt = open(file_path, "w")
    newLogTxt.write("TimeStamp\tPlataform\tLogType\tMessage\tProcessID\tProcessConfigurationName\n")
    allLogs = requests.get(creds['url'] + f"/odata/RobotLogs?$filter=JobKey eq {key} ", headers=header)
    countAllLogs = allLogs.json()['@odata.count']
    for log in range(0, countAllLogs):
        message = str(allLogs.json()['value'][log]['Message'])
        logType = str(allLogs.json()['value'][log]['Level'])
        timeStampNeedsFixing = str(allLogs.json()['value'][log]['TimeStamp'])
        timeStampDate = timeStampNeedsFixing.split("T")[0]
        timeStampTime = timeStampNeedsFixing.split("T")[1]

        miliseconds = timeStampTime  # .split(".")[1]

        # if len(miliseconds)!= 4:
        #     miliseconds = miliseconds.replace("Z","")
        #     print(miliseconds)
        #     while len(miliseconds)!=3:
        #         miliseconds +="0"
        #     miliseconds+="Z"

        newLogTxt.write(
            timeStampDate + " " + timeStampTime + "\t" + "Uipath Orchestrator" + "\t" + logType + "\t" + message + "\t" + str(
                newQueueProcess.id) + "\t" + newQueueProcess.idConfiguration.name + "\n")

    newLogTxt.close()
    sort_file_by_time(file_path)
    with open(file_path, "rb") as file:
        log_file = File(file)
        Log.objects.create(
            idProcess=newQueueProcess,
            ficheiro=log_file,
            date=datetime.now()
        )

    if os.path.exists(file_path):
        os.remove(file_path)


def extract_time(line):
    time_start = line.find('2')
    time_end = line.find('\t')
    return line[time_start:time_end]


def sort_file_by_time(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sorted_lines = sorted(lines, key=extract_time)

    with open(file_path, 'w') as file:
        file.writelines(sorted_lines)

# -------------- End Other functions --------------- #
