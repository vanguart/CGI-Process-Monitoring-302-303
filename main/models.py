from datetime import datetime
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


class SLA(models.Model):
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=600)
    idTask = models.ForeignKey('QueueTask', on_delete=models.CASCADE, related_name='SlaTask')

    def __str__(self):
        return f"{self.startDate} - {self.endDate}"


class ProcessType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ProcessConfiguration(models.Model):
    name = models.CharField(max_length=256)
    idProcessType = models.ForeignKey(ProcessType, on_delete=models.CASCADE, related_name='processType')
    description = models.CharField(max_length=500)
    maxTimeSla = models.TimeField(null=True)
    idTeam = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='ProcessConfigurationTeam')
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
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    state = models.CharField(max_length=256)
    idLabels = models.ManyToManyField(Label, related_name="labels", blank=True)
    idUser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userProfile')

    def __str__(self):
        return str(self.idConfiguration)


class TaskConfiguration(models.Model):
    idProcessConfiguration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE,
                                               related_name='processConfiguration')
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    idtaskType = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='taskType')
    maxTimeSla = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class QueueTask(models.Model):
    idTaskConfiguration = models.ForeignKey(TaskConfiguration, on_delete=models.CASCADE,
                                            related_name="taskConfiguration")
    idProcess = models.ForeignKey('QueueProcess', on_delete=models.CASCADE, related_name="process")
    priority = models.IntegerField()
    state = models.CharField(max_length=256)

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
    now = datetime.now()
    return f"Logs/{now.year}/{now.month}/{now.day}/{now.strftime('%H-%M')}_{instance.task.id}.txt"


class LogType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Log(models.Model):
    logType = models.ForeignKey(LogType, on_delete=models.CASCADE, related_name='logType')
    task = models.ForeignKey(QueueTask, on_delete=models.CASCADE, related_name='task')
    ficheiro = models.FileField(upload_to=log_path, max_length=254)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.logType}"


class Reporting(models.Model):
    tasks = models.ForeignKey(QueueTask, on_delete=models.CASCADE, related_name="reportingTasks")
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.description
