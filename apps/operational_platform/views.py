from django.shortcuts import render

# Create your views here.

def businessExceptions_page_view(request):
	return render(request, 'operational_platform/businessExceptions.html')

def correcaoDocumentos_page_view(request):
	return render(request, 'operational_platform/correcaoDocumentos.html')

def reportarErrosNoSistema_page_view(request):
	return render(request, 'operational_platform/reportarErrosNoSistema.html')