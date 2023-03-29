from datetime import datetime
from django.db import models


# Create your models here.
# Back-end

class Permition(models.Model):
    functionality = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.functionality}"


class Label(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"
    


class Perfil(models.Model):
    type = models.CharField(max_length=256)
    permitionPerfil = models.ManyToManyField(Permition, related_name='permitionPerfil')

    def __str__(self):
        return f"{self.type}"


class TaskType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


# class SLO(models.Model):
#    punish = models.CharField(max_length=200)
#    reason = models.CharField(max_length=200)
#    condition = models.CharField(max_length=200)

class SLA(models.Model):
    inicialDate = models.DateField(null=True)
    finalDate = models.DateField(null=True)

    def __str__(self):
        return f"{self.inicialDate} - {self.finalDate}"


class LogsType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} -> {self.name}"


class ProcessType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class User(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    goal = models.IntegerField(default=0)
    idPerfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    
    
class ProcessConfiguration(models.Model):
    name = models.CharField(max_length=256)
    idProcessType = models.ForeignKey(ProcessType, on_delete=models.CASCADE)
    idSLA = models.ForeignKey(SLA, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    maxTimeSLA = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name}"


class Process(models.Model):
    idProcessConfiguration = models.ForeignKey(ProcessConfiguration, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    inicialDate = models.DateField(null=True)
    finalDate = models.DateField(null=True)
    state = models.CharField(max_length=256)
    label = models.ManyToManyField(Label, related_name='label')


    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    teamName = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    team = models.ManyToManyField(User, related_name='team')
    permitionTeam = models.ManyToManyField(Permition, related_name='permitionTeam')

    def __str__(self):
        return f"{self.teamName}"


class Task_Configuration(models.Model):
    idProcessConfiguration = models.ForeignKey(Process, on_delete=models.CASCADE)
    idSLA = models.ForeignKey(SLA, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    taskType = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    maxTimeSLA = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} -> {self.description}"



class Task(models.Model):
    idTaskConfiguration = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="idTaskConfiguration")
    idProcess = models.ForeignKey(Process, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField()
    state = models.CharField(max_length=256)
    team = models.ManyToManyField(Team, related_name="tasks")
    inicialDate = models.DateField(null=True)
    finalDate = models.DateField(null=True)

    def __str__(self):
        return f"{self.name} -> {self.description}"


def path(id_log):
    current_time = datetime.now().strftime('%H:%M') 
    return f"Logs/% Y/% m/% d/{current_time}_${id_log}.txt"
        


class Logs(models.Model):  # users also make logs
    idLogType = models.ForeignKey(LogsType, on_delete=models.CASCADE)
    idTask = models.ForeignKey(Task, on_delete=models.CASCADE)
    ficheiro = models.FileField(upload_to =path(idTask), max_length=254, )

    def __str__(self):
        return f"{self.idLogType} -> {self.description}"