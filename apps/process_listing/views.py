from django.shortcuts import render

# Create your views here.

def process_listing_page_view(request):
    return render(request, 'process_listing/process_listing.html')