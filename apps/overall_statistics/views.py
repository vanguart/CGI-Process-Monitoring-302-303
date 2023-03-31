from django.shortcuts import render

# Create your views here.
def todoAnalyst_page_view(request):
	return render(request, 'overall_statistics/todoAnalysts.html')