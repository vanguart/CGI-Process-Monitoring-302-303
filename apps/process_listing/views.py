from django.shortcuts import render
from main.models import Process, Label
# Create your views here.

def process_listing_page_view(request):

    if request.GET.get('filtros') == "noFilter" :
        query = Process.objects.all()

    if request.GET.get('filtros') != "noFilter":
        featured_filter = request.GET.get('filtros')
        query = Process.objects.filter(label__name=featured_filter)


    context = {
        'process': query,
        'filtros': Label.objects.all(),
    }
    
    return render(request, 'process_listing/process_listing.html', context)