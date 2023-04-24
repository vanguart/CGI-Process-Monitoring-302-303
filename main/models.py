from datetime import datetime
from django.contrib.auth.models import User, Group
from django.db import models


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

    def __str__(self):
        return f"{self.startDate} - {self.endDate}"


class ProcessType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    recoveryCode = models.CharField(max_length=10, blank=True)
    goal = models.IntegerField(default=100)
    groupUser = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groupUser")
    lastCodeSentTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = [
            ("access_admin_page", "Can access the admin page"),
            ("access_analytic_page", "Can access the analytic page"),
            ("access_operational_page", "Can access the operational page"),
        ]


class ProcessConfiguration(models.Model):
    name = models.CharField(max_length=256)
    processType = models.ForeignKey(ProcessType, on_delete=models.CASCADE, related_name='processType')
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE, related_name='ProcessConfigurationSla')
    description = models.CharField(max_length=500)
    maxTimeSla = models.TimeField(null=True)

    def __str__(self):
        return self.name


class Process(models.Model):
    configuration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE, related_name='configuration')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='processUser')
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    state = models.CharField(max_length=256)
    labels = models.ManyToManyField(Label, related_name="labels", blank=True)

    def __str__(self):
        return str(self.configuration)


class TaskConfiguration(models.Model):
    processConfiguration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE,
                                             related_name='processConfiguration')
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE, related_name='TaskConfigurationSla')
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    taskType = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name='taskType')
    maxTimeSla = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class Task(models.Model):
    configuration = models.ForeignKey(TaskConfiguration, on_delete=models.CASCADE, related_name="taskConfiguration")
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="process")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='taskUser',null=True,blank=True)
    priority = models.IntegerField()
    state = models.CharField(max_length=256)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)

    def __str__(self):
        return str(self.configuration)


class Team(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    members = models.ManyToManyField(UserProfile, related_name='members')
    permissions = models.ManyToManyField(Group, related_name='teamPermissions')
    tasks = models.ManyToManyField(Task, related_name="tasks")
    teamLider = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="teamLider")


    def __str__(self):
        return self.name


def log_path(instance,filename):
    now = datetime.now()
    return f"Logs/{now.year}/{now.month}/{now.day}/{now.strftime('%H-%M')}_{instance.task.id}.txt"


class LogType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Log(models.Model):
    logType = models.ForeignKey(LogType, on_delete=models.CASCADE, related_name='logType')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    ficheiro = models.FileField(upload_to=log_path, max_length=254)

    def __str__(self):
        return f"{self.logType}"
    
    
class Reporting(models.Model):
    tasks = models.ManyToManyField(Task, related_name="reportingTasks")
    description = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.description
