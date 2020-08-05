from django.shortcuts import render
from django.http import JsonResponse

from ecfgrades.grades.models import Grade


# -----------------------------------------------------------------------------
def index(request):
    return render(request, 'statistics/index.html')


# -----------------------------------------------------------------------------
def distrib(request):
    data = (Grade.objects.
            filter(grading_date='2020-07-01').
            exclude(grade__isnull=True).
            values_list('grade', flat=True))

    return JsonResponse(list(data), safe=False)
