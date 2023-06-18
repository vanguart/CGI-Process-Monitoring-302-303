from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required("main.access_analytic_page")
def statistics_page_view(request):
    return render(request, 'overall_statistics/statistics.html')
