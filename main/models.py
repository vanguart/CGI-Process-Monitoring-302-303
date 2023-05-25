from django.contrib.auth.models import User, Group
from django.db import models


class Skill(models.Model):
    nameSkill = models.CharField(max_length=256)

    def __str__(self):
        return self.nameSkill


class Label(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ProcessType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ProcessConfiguration(models.Model):
    name = models.CharField(max_length=256)
    idProcessType = models.ForeignKey(ProcessType, on_delete=models.CASCADE, related_name='processType')
    description = models.CharField(max_length=500)
    maxTimeKPI = models.DurationField(null=True)
    idTeam = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='ProcessConfigurationTeam', blank=True,
                               null=True)
    idSkills = models.ManyToManyField(Skill, related_name='ProcessConfigurationSkill')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    idUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    recoveryCode = models.CharField(max_length=10, blank=True)
    goal = models.IntegerField(default=100)
    idGroupUser = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groupUser")
    lastCodeSentTime = models.DateTimeField(null=True, blank=True)
    idTeam = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="equipaMembros", blank=True, null=True)
    idSkills = models.ManyToManyField(Skill, related_name="skillUser")

    def __str__(self):
        return self.idUser.username

    class Meta:
        permissions = [
            ("access_admin_page", "Can access the admin page"),
            ("access_analytic_page", "Can access the analytic page"),
            ("access_operational_page", "Can access the operational page"),
        ]


class QueueProcess(models.Model):
    idConfiguration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE, related_name='configuration')
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    registerDate = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=256, default="Completed")
    idLabels = models.ManyToManyField(Label, related_name="labels", blank=True)
    idUser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userProfile', blank=True, null=True)

    def __str__(self):
        return str(self.idConfiguration)


class TaskConfiguration(models.Model):
    idProcessConfiguration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE,
                                               related_name='processConfiguration')
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    idtaskType = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='taskType')
    maxTimeKPI = models.DurationField(null=True)
    responsibility = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.description}"


class QueueTask(models.Model):
    idTaskConfiguration = models.ForeignKey(TaskConfiguration, on_delete=models.CASCADE,
                                            related_name="taskConfiguration")
    idProcess = models.ForeignKey('QueueProcess', on_delete=models.CASCADE, related_name="process")
    priority = models.IntegerField()
    state = models.CharField(max_length=256, default="Completed")
    startDate = models.DateTimeField(null=True, blank=True)
    startWorkingDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.idTaskConfiguration)


class Team(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    idPermissions = models.ManyToManyField(Group, related_name='teamPermissions')
    idTeamLider = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="teamLider", null=True)
    idSkils = models.ManyToManyField(Skill, related_name="skills")

    def __str__(self):
        return self.name


def log_path(instance, filename):
    date = instance.idProcess.startDate
    dateSplit = date.split(" ")
    year = dateSplit[0].split("-")[0]
    month = dateSplit[0].split("-")[1]
    day = dateSplit[0].split("-")[2]

    hour = dateSplit[1].split(":")[0]
    mins = dateSplit[1].split(":")[1]
    return f"apps/logs/logData/process-monitor-{year}-{month}-{day}-{hour}-{mins}_{instance.idProcess.id}.log"


class Log(models.Model):
    idProcess = models.ForeignKey(QueueProcess, on_delete=models.CASCADE, related_name='LogProcess')
    ficheiro = models.FileField(upload_to=log_path, max_length=254)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Log do {self.idProcess}"


class Reporting(models.Model):
    idUser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="reportingUser")
    description = models.CharField(max_length=2000)
    ficheiro = models.FileField(upload_to="static/files/ReportingErros/", max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.idUser} -> {self.description[0:50]}"


class TaskData(models.Model):
    idTask = models.ForeignKey('QueueTask', on_delete=models.CASCADE, related_name="taskData")
    inputData = models.CharField(blank=True, max_length=10000)
    outputData = models.CharField(blank=True, max_length=10000)
    errorMessage = models.CharField(default="No error or warning in this queueTasks", max_length=10000)

    def __str__(self):
        return str(self.id)
