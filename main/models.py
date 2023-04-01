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
    initial_date = models.DateField(null=True)
    final_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.initial_date} - {self.final_date}"


class LogType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ProcessType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    goal = models.IntegerField(default=100)
    profile_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return self.user.name

    class Meta:
        permissions = [
            ("access_admin_page", "Can access the admin page"),
            ("access_analytic_page", "Can access the analytic page"),
            ("access_operational_page", "Can access the operational page"),
        ]


class ProcessConfiguration(models.Model):
    name = models.CharField(max_length=256)
    process_type = models.ForeignKey(ProcessType, on_delete=models.CASCADE)
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    max_time_sla = models.TimeField(null=True)

    def __str__(self):
        return self.name


class Process(models.Model):
    configuration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    initial_date = models.DateField(null=True)
    final_date = models.DateField(null=True)
    state = models.CharField(max_length=256)
    labels = models.ManyToManyField(Label, related_name="labels", blank=True)

    def __str__(self):
        return str(self.configuration)


class Team(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    members = models.ManyToManyField(UserProfile, related_name='members')
    permissions = models.ManyToManyField(Group, related_name='permissions')

    def __str__(self):
        return self.name


class TaskConfiguration(models.Model):
    process_configuration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE)
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    max_time_sla = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class Task(models.Model):
    configuration = models.ForeignKey(TaskConfiguration, on_delete=models.CASCADE, related_name="tasksConfiguration")
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="process")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    priority = models.IntegerField()
    state = models.CharField(max_length=256)
    team = models.ManyToManyField(Team, related_name="team")
    initial_date = models.DateField(null=True)
    final_date = models.DateField(null=True)

    def __str__(self):
        return str(self.configuration)


def log_path(id_log):
    now = datetime.now()
    return f"Logs/{now.year}/{now.month}/{now.day}/{now.strftime('%HH:%MM')}_${id_log}.txt"


class Log(models.Model):
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    ficheiro = models.FileField(upload_to=log_path(task), max_length=254)

    def __str__(self):
        return f"{self.idLogType} -> {self.description}"
