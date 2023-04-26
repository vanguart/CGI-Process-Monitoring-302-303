from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import QueueProcess, Label
# Create your views here.

def process_listing_page_view(request):

    if request.GET.get('filtros') == None:
        query = QueueProcess.objects.all()
    else:
        if request.GET.get('filtros') == "noFilter" :
            query = QueueProcess.objects.all()

        if request.GET.get('filtros') != "noFilter":
            featured_filter = request.GET.get('filtros')
            query = QueueProcess.objects.filter(labels__name=featured_filter)



    context = {
        'process': query,
        'filtros': Label.objects.all(),
        # DEBUGG FILTER TYPE ->  'tipoDeFiltro': request.GET.get('filtros')
    }
    
    return render(request, 'process_listing/process_listing.html', context)