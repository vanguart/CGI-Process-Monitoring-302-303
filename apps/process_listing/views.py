from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import QueueProcess, Label, QueueTask, ProcessConfiguration


# Create your views here.
def process_listing_page_view(request):
    processTasks = {}

    for process in QueueProcess.objects.all():
        for task in QueueTask.objects.all():
            if process.id == task.idProcess:
                processTasks.update

    if request.GET.get('filtros') is None and request.GET.get('estados') is None:
        query = QueueProcess.objects.all()
    else:

        if request.GET.get('filtros') == "noFilter" or request.GET.get('estados') == "noState":
            query = QueueProcess.objects.all()

        if request.GET.get('filtros') != "noFilter" and request.GET.get('estados') is None:
            featuredFilter = request.GET.get('filtros')
            query = QueueProcess.objects.filter(idLabels__name=featuredFilter)

        if request.GET.get('estados') != "noState" and request.GET.get('filtros') is None:
            featuredFilter = request.GET.get('estados')
            query = QueueProcess.objects.filter(state=featuredFilter)

        #Após design
        #processos config1       processos config2
        #proc1                  proc3
        #proc2                  proc4

        #Agora
        # processos config
        # proc1
        # proc2

        # processos config2
        # proc3
        # proc4

    context = {
        'processesConfiguration': ProcessConfiguration.objects.all(),
        'processes': query,
        'states': QueueProcess.objects.values_list('state', flat=True).distinct(),
        'filtros': Label.objects.all(),
        'tasks': QueueTask.objects.all(),
    }

    return render(request, 'process_listing/process_listing.html', context)
