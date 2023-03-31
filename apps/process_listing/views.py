from django.shortcuts import render
from main.models import Process
# Create your views here.

def process_listing_page_view(request):
    context = {'process': Process.objects.all()}
    
    return render(request, 'process_listing/process_listing.html', context)