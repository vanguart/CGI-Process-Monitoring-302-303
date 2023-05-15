from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import QueueProcess, Label, QueueTask


# Create your views here.
def process_listing_page_view(request):
    processTasks = {}

    for process in QueueProcess.objects.all():
        for task in QueueTask.objects.all():
            if process.id == task.idProcess:
                processTasks.update

    if request.GET.get('filtros') is None:
        query = QueueProcess.objects.all()
    else:
        if request.GET.get('filtros') == "noFilter":
            query = QueueProcess.objects.all()

        if request.GET.get('filtros') != "noFilter":
            featuredFilter = request.GET.get('filtros')
            query = QueueProcess.objects.filter(idLabels__name=featuredFilter)

    context = {
        'processes': query,
        'filtros': Label.objects.all(),
        'tasks': QueueTask.objects.all(),
        # DEBUGG FILTER TYPE ->  'tipoDeFiltro': request.GET.get('filtros')
    }

    return render(request, 'process_listing/process_listing.html', context)
