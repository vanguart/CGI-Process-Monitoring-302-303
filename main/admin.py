from django.contrib import admin

# Register your models here.
# from .models import Permition
# from .models import Perfil
from .models import Team
from .models import TaskType
from .models import SLA
from .models import LogsType
from .models import ProcessType
from .models import User
from .models import Process
from .models import Task
from .models import Logs
from .models import Label
from .models import ProcessConfiguration
from .models import Task_Configuration


class PerfilHorizontal(admin.ModelAdmin):
    filter_horizontal = ("permitionPerfil",)


class TeamHorizontal(admin.ModelAdmin):
    filter_horizontal = ("team", "tasks")


class ProcessesHorizontal(admin.ModelAdmin):
    filter_horizontal = ("label",)


# admin.site.register(Permition)
admin.site.register(Label)
# admin.site.register(Perfil, PerfilHorizontal)
admin.site.register(TaskType)
admin.site.register(SLA)
admin.site.register(LogsType)
admin.site.register(ProcessType)
admin.site.register(User)
admin.site.register(Process, ProcessesHorizontal)
admin.site.register(Task)
admin.site.register(Team, TeamHorizontal)
admin.site.register(Logs)
admin.site.register(ProcessConfiguration)
admin.site.register(Task_Configuration)
