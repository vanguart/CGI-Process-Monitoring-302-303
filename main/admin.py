from django.contrib import admin

# Register your models here.
from .models import Team, Skill
from .models import TaskType
from .models import ProcessType
from .models import UserProfile
from .models import QueueProcess
from .models import QueueTask
from .models import Log
from .models import Label
from .models import ProcessConfiguration
from .models import TaskConfiguration
from .models import Reporting
from .models import TaskData


class TeamHorizontal(admin.ModelAdmin):
    filter_horizontal = ("idPermissions", "idSkils",)


class QueueProcessesHorizontal(admin.ModelAdmin):
    filter_horizontal = ("idLabels",)


class ProcessesConfigurationHorizontal(admin.ModelAdmin):
    filter_horizontal = ("idSkills",)


class UserProfileHorizontal(admin.ModelAdmin):
    filter_horizontal = ("idSkills",)


admin.site.register(Label)
admin.site.register(Skill)
admin.site.register(Team, TeamHorizontal)
admin.site.register(Log)
admin.site.register(UserProfile, UserProfileHorizontal)
admin.site.register(Reporting)

admin.site.register(TaskType)
admin.site.register(ProcessType)
admin.site.register(QueueProcess, QueueProcessesHorizontal)
admin.site.register(QueueTask)
admin.site.register(ProcessConfiguration, ProcessesConfigurationHorizontal)
admin.site.register(TaskConfiguration)
admin.site.register(TaskData)