from datetime import datetime as dt
from django.shortcuts import get_object_or_404, render

from .models import Player, Grade
from .forms import PlayerForm


# -------------------------------------------------------------------------
def index(request):
    grades = []
    timepoint = None
    if request.method == 'POST':
        form = PlayerForm(request.POST, label_suffix='')
        if form.is_valid():
            # ChoiceField in forms produces strings
            timepoint = dt.strptime(form.cleaned_data['timepoint'], '%Y-%m-%d')
            grades = (Grade.objects.
                      filter(grading_date=timepoint).
                      filter(player__name__icontains=form.cleaned_data['name']).
                      order_by('player__name'))
    else:
        form = PlayerForm()

    context = {'grades': grades[:100], 'timepoint': timepoint, 'form': form}
    return render(request, 'grades/index.html', context)


# -------------------------------------------------------------------------
def detail(request, player_ref):
    player = get_object_or_404(Player, pk=player_ref)
    return render(request, 'grades/detail.html', {'player': player})
