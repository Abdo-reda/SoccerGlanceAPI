from django import forms
from .models import Match, League

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class MatchForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Match
        fields = ['match_link', 'league', 'team_1', 'team_2', 'date', 'time']
        exclude = ['score', 'is_live', 'is_user_uploaded']

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['league'].choices = [('', 'Select League')] + [(league.league_id, str(league)) for league in League.objects.all()]
        self.fields['match_link'].widget.attrs['class'] = 'form-control'
        self.fields['league'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['time'].widget.attrs['class'] = 'form-control'
        self.fields['team_1'].widget.attrs['class'] = 'form-control'
        self.fields['team_2'].widget.attrs['class'] = 'form-control'
        self.fields['league'].empty_label = 'Select League'

