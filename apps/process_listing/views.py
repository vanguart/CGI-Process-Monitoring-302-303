from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import Process, Label
# Create your views here.

def process_listing_page_view(request):

    if request.GET.get('filtros') == None:
        query = Process.objects.all()
    else:
        if request.GET.get('filtros') == "noFilter" :
            query = Process.objects.all()

        if request.GET.get('filtros') != "noFilter":
            featured_filter = request.GET.get('filtros')
            query = Process.objects.filter(label__name=featured_filter)



    context = {
        'process': query,
        'filtros': Label.objects.all(),
        # DEBUGG FILTER TYPE ->  'tipoDeFiltro': request.GET.get('filtros')
    }
    
    return render(request, 'process_listing/process_listing.html', context)