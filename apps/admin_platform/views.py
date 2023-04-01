from django.shortcuts import render

# Create your views here.
def todoAdmin_page_view(request):
	return render(request, 'admin_platform/todoAdmin.html')