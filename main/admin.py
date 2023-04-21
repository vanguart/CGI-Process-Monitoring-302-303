from django.contrib import admin

# Register your models here.
from .models import Team
from .models import TaskType
from .models import SLA
from .models import LogType
from .models import ProcessType
from .models import UserProfile
from .models import Process
from .models import Task
from .models import Log
from .models import Label
from .models import ProcessConfiguration
from .models import TaskConfiguration
from .models import Reporting


class TeamHorizontal(admin.ModelAdmin):
    filter_horizontal = ("members", "tasks", "permissions")


class ProcessesHorizontal(admin.ModelAdmin):
    filter_horizontal = ("labels",)
    
class ReportingHorizontal(admin.ModelAdmin):
    filter_horizontal = ("tasks",)


# admin.site.register(Permition)
admin.site.register(Label)
# admin.site.register(Perfil, PerfilHorizontal)
admin.site.register(TaskType)
admin.site.register(SLA)
admin.site.register(LogType)
admin.site.register(ProcessType)
admin.site.register(UserProfile)
admin.site.register(Process, ProcessesHorizontal)
admin.site.register(Task)
admin.site.register(Team, TeamHorizontal)
admin.site.register(Log)
admin.site.register(ProcessConfiguration)
admin.site.register(TaskConfiguration)
admin.site.register(Reporting, ReportingHorizontal)
