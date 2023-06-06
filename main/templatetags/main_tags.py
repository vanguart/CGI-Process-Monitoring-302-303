import os
from django import template
from main.models import *


register = template.Library()

@register.simple_tag
def get_reportingCount():

    allReportssDataBaseNUMBER = Reporting.objects.all().count()

    return allReportssDataBaseNUMBER


@register.simple_tag
def get_reportingData():

    reportingObjects = Reporting.objects.all()

    listaReportingObjects = list(reportingObjects)

    for obj in listaReportingObjects:
        obj.file_name = os.path.basename(obj.ficheiro.name) if obj.ficheiro else None


    return listaReportingObjects
