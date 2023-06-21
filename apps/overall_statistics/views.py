from django.shortcuts import render


# Create your views here.
def statistics_page_view(request):

    context = {
    }

    return render(request, 'overall_statistics/statistics.html', context)
