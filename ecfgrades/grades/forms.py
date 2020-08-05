from django import forms
from .models import Grade


# -------------------------------------------------------------------------
def get_timepoints():
    return [
        (t, t.strftime('%b %Y'))
        for t in (Grade.objects.
                  distinct().
                  order_by('-grading_date').
                  values_list('grading_date', flat=True))
    ]


# -------------------------------------------------------------------------
class PlayerForm(forms.Form):
    name = forms.CharField(label='Player name', max_length=100)
    timepoint = forms.ChoiceField(label='Year/month', choices=get_timepoints())
