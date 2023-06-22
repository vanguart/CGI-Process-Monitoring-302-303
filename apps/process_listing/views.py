from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import QueueProcess, Label, QueueTask, ProcessConfiguration,Log
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required("main.access_analytic_page")
def process_listing_page_view(request):
    if request.GET.get('filtros') is None:
        query = ProcessConfiguration.objects.all()
    else:
        if request.GET.get('filtros') == "noFilter":
            query = ProcessConfiguration.objects.all()

        if request.GET.get('filtros') != "noFilter":
            featuredFilter = request.GET.get('filtros')
            query = ProcessConfiguration.objects.filter(idLabels__name=featuredFilter)

    context = {
        'processesConfiguration': query,
        'processes': QueueProcess.objects.all(),
        'filtros': Label.objects.all(),
        'tasks': QueueTask.objects.all(),
        'logs': Log.objects.all()
    }

    return render(request, 'process_listing/process_listing.html', context)
